from mango_server.utils.aiohttp_utils import get_request_with_query
from mango_server.config import S2_API_KEY


desired_fiels = [
    'title', 'paperId', 'url', 'citationCount', 'year',
    'isInfluential', 'contexts', 'intents'
]


async def get_paper_influential_references_and_citations(paper_id: str):
    """Get influential references and citations of a paper"""
    # Fetch citations
    raw_citations = await get_request_with_query(
        request_url=f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations",
        request_query={
            "fields": ",".join(desired_fiels),
            "offset": 0,
            "limit": 1000
        },
        request_header={
            "X-API-Key": S2_API_KEY
        }
    )
    influential_citations = [
        paper
        for paper in raw_citations["data"]
        if paper["isInfluential"] and paper['citingPaper']['citationCount'] > 0
    ]
    citations_data = sorted(
        influential_citations,
        key=lambda x: x['citingPaper']['citationCount'],
        reverse=True
    )
    # Fetch references
    raw_references = await get_request_with_query(
        request_url=f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references",
        request_query={
            "fields": ",".join(desired_fiels),
            "offset": 0,
            "limit": 1000
        },
        request_header={
            "X-API-Key": S2_API_KEY
        }
    )
    influential_references = [
        paper
        for paper in raw_references["data"]
        if paper["isInfluential"]
    ]
    references_data = sorted(
        influential_references,
        key=lambda x: x['citedPaper']['citationCount'],
        reverse=True
    )
    # Form result
    ret = {
        "citations": citations_data,
        "references": references_data
    }

    return ret
