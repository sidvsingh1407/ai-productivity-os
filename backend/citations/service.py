from typing import List
from regulation.schemas import SearchResponseItem
from citations.schemas import Citation

class CitationFormatterService:
    def format_citations(self, chunks: List[SearchResponseItem]) -> List[Citation]:
        citations = []
        for chunk in chunks:
            if chunk.article_number and chunk.section_title:
                citation_str = f"EU AI Act, Article {chunk.article_number} - {chunk.section_title}"
            elif chunk.article_number:
                citation_str = f"EU AI Act, Article {chunk.article_number}"
            elif chunk.section_title:
                citation_str = f"EU AI Act, {chunk.section_title}"
            else:
                citation_str = "Source: EU AI Act [unspecified section]"

            citations.append(
                Citation(
                    chunk_text=chunk.chunk_text,
                    citation=citation_str,
                    article_number=chunk.article_number,
                    section_title=chunk.section_title,
                    relevance_score=chunk.relevance_score,
                )
            )
        return citations
