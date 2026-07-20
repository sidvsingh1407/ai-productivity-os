import asyncio
import os
import re
import logging
from typing import List, Dict

from database import async_session_maker
from models.regulation_chunk import RegulationChunk
from utils.gemini_client import embed_text
import sqlalchemy as sa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SOURCE_NAME = "eu_ai_act"
SOURCE_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "eu_ai_act_source.md")

def parse_markdown(text: str) -> List[Dict[str, str]]:
    """
    Splits the EU AI Act Markdown into chunks based on headers.
    Returns a list of dicts with keys: article_number, section_title, content.
    """
    chunks = []

    # Split text by Markdown headers
    # We look for lines starting with '## Chapter', '## Article', or '## Annex'

    # First, split the document by any major header to easily isolate them
    sections = re.split(r'\n(?=##\s+(?:Chapter|Article|Annex|Recital))', '\n' + text)

    current_chapter = None

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split('\n')
        header_line = lines[0].strip()

        if header_line.startswith('## Chapter'):
            # Update current chapter title for context, but we don't treat this as a separate chunk
            # Usually Chapters contain Articles
            current_chapter = header_line.replace('## ', '').strip()
            continue

        elif header_line.startswith('## Recital'):
            # Lower priority, keep as a large chunk or skip. For now, keep as a coarse chunk.
            article_num = header_line.replace('## Recital', 'Recital').strip()
            title = current_chapter if current_chapter else "Recital"
            chunks.append({
                "article_number": article_num,
                "section_title": title,
                "content": section
            })

        elif header_line.startswith('## Article'):
            # Parse article number and title
            match = re.match(r'##\s+Article\s+(\d+)\s*(?:[-—–]\s*(.*))?', header_line)
            if match:
                article_num = match.group(1)
                title = match.group(2) if match.group(2) else ""
            else:
                article_num = header_line.replace('## Article', '').strip()
                title = ""

            # If the article is very long, we should chunk by paragraph
            # We assume paragraphs start with '1.', '2.', '3.' or '(a)', '(b)'
            paragraphs = re.split(r'\n(?=\d+\.\s)', section)

            if len(paragraphs) > 1:
                # The first item might just be the article header itself, which shouldn't be a standalone chunk
                for i, para in enumerate(paragraphs):
                    para = para.strip()
                    if not para or para == header_line:
                        continue

                    sub_num = article_num

                    # Try to parse the paragraph number
                    para_match = re.match(r'^(\d+)\.', para)
                    if para_match:
                        sub_num = f"{article_num}({para_match.group(1)})"

                    chunks.append({
                        "article_number": sub_num,
                        "section_title": title,
                        # If this isn't the first item, or if it doesn't start with the header, inject the header for context
                        "content": para if header_line in para else f"{header_line}\n\n{para}"
                    })
            else:
                # Single chunk for the whole article
                chunks.append({
                    "article_number": article_num,
                    "section_title": title,
                    "content": section
                })

        elif header_line.startswith('## Annex'):
            match = re.match(r'##\s+Annex\s+([IXV]+)\s*(?:[-—–]\s*(.*))?', header_line)
            if match:
                annex_num = f"Annex {match.group(1)}"
                title = match.group(2) if match.group(2) else ""
            else:
                annex_num = header_line.replace('## ', '').strip()
                title = ""

            chunks.append({
                "article_number": annex_num,
                "section_title": title,
                "content": section
            })

    return chunks

async def ingest_eu_ai_act():
    """Reads the EU AI Act Markdown, chunks it, generates embeddings, and saves to DB."""
    if not os.path.exists(SOURCE_FILE_PATH):
        logger.error(f"Source file not found at {SOURCE_FILE_PATH}. Skipping ingestion.")
        return

    logger.info(f"Reading source file {SOURCE_FILE_PATH}...")
    with open(SOURCE_FILE_PATH, 'r', encoding='utf-8') as f:
        text = f.read()

    logger.info("Parsing and chunking Markdown...")
    chunks_data = parse_markdown(text)
    logger.info(f"Generated {len(chunks_data)} chunks.")

    async with async_session_maker() as session:
        # Idempotency: clear existing chunks for this source
        logger.info(f"Clearing existing chunks for source '{SOURCE_NAME}'...")
        await session.execute(sa.delete(RegulationChunk).where(RegulationChunk.source == SOURCE_NAME))
        await session.commit()

        logger.info("Generating embeddings and inserting chunks...")
        for i, data in enumerate(chunks_data):
            try:
                # This call is synchronous, wrap in to_thread if running in strict async loop,
                # but since this is a script, we can just block or use asyncio.to_thread
                embedding = await asyncio.to_thread(embed_text, data["content"])

                chunk = RegulationChunk(
                    source=SOURCE_NAME,
                    article_number=data["article_number"],
                    section_title=data["section_title"],
                    content=data["content"],
                    embedding=embedding
                )
                session.add(chunk)

                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(chunks_data)} chunks...")
                    await session.commit()
            except Exception as e:
                logger.error(f"Failed to process chunk {data.get('article_number')}: {e}")

        await session.commit()
        logger.info("Ingestion completed successfully.")

if __name__ == "__main__":
    asyncio.run(ingest_eu_ai_act())
