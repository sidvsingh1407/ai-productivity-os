from regulation.schemas import SearchResponseItem
from citations.service import CitationFormatterService

def test_citations_both_fields_present():
    service = CitationFormatterService()
    chunks = [
        SearchResponseItem(
            chunk_text="This is a test chunk.",
            article_number="6(1)",
            section_title="Risk Classification",
            relevance_score=0.95
        )
    ]
    citations = service.format_citations(chunks)
    assert len(citations) == 1
    assert citations[0].citation == "EU AI Act, Article 6(1) - Risk Classification"
    assert citations[0].chunk_text == "This is a test chunk."
    assert citations[0].relevance_score == 0.95

def test_citations_only_article_present():
    service = CitationFormatterService()
    chunks = [
        SearchResponseItem(
            chunk_text="Another chunk.",
            article_number="5",
            section_title=None,
            relevance_score=0.88
        )
    ]
    citations = service.format_citations(chunks)
    assert len(citations) == 1
    assert citations[0].citation == "EU AI Act, Article 5"

def test_citations_only_section_present():
    service = CitationFormatterService()
    chunks = [
        SearchResponseItem(
            chunk_text="Yet another chunk.",
            article_number=None,
            section_title="Annex IV",
            relevance_score=0.90
        )
    ]
    citations = service.format_citations(chunks)
    assert len(citations) == 1
    assert citations[0].citation == "EU AI Act, Annex IV"

def test_citations_neither_present():
    service = CitationFormatterService()
    chunks = [
        SearchResponseItem(
            chunk_text="Fallback chunk.",
            article_number=None,
            section_title=None,
            relevance_score=0.75
        )
    ]
    citations = service.format_citations(chunks)
    assert len(citations) == 1
    assert citations[0].citation == "Source: EU AI Act [unspecified section]"

def test_citations_empty_list():
    service = CitationFormatterService()
    chunks = []
    citations = service.format_citations(chunks)
    assert len(citations) == 0
