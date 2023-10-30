from fastapi import APIRouter

from mango_server.paper.graph import get_paper_influential_references_and_citations
from mango_server.paper.info import get_single_paper_info_with_id, get_paper_details_in_batch_with_ids


paper_router = APIRouter(
    prefix="/paper",
    tags=["paper"],
)


@paper_router.get("/details/{paper_id}")
async def get_single_paper_details(paper_id: str):
    data = await get_single_paper_info_with_id(paper_id=paper_id)

    return data


@paper_router.post("/batch")
async def get_batch_paper_details(paper_ids: list[str]):
    data = await get_paper_details_in_batch_with_ids(paper_ids=paper_ids)

    return data


@paper_router.get("/graph/{paper_id}")
async def get_paper_graph(paper_id: str):
    data = await get_paper_influential_references_and_citations(paper_id=paper_id)

    return data
