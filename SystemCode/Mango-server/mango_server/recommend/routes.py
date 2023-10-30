from fastapi import APIRouter

from mango_server.domain.user import UserQuery
from mango_server.recommend.dual_tower import get_top_candidates_for_user
from mango_server.recommend.index import query_with_bf_index
from mango_server.recommend.s2_wrapper import get_paper_recommendation_for_single_pos
from mango_server.recommend.embedding import get_papers_with_embedding

recommend_router = APIRouter(
    prefix="/recommend",
    tags=["recommend"],
)


@recommend_router.get("/dual")
async def get_recommendation_for_user(user_id: str, top_k: int = 10):
    data = await get_top_candidates_for_user(
        user_id=user_id,
        num_candidate=top_k
    )

    return data


@recommend_router.post("/dual/v2")
async def get_dual_recommendation_for_user(user_query: UserQuery):
    data = await query_with_bf_index(
        raw_query=user_query.dict(),
        top_k=10
    )

    return data


@recommend_router.get("/s2/{paper_id}")
async def get_single_recommendation_for_paper(
        paper_id: str, top_k: int = 10, source: str = "recent"
):
    data = await get_paper_recommendation_for_single_pos(
        paper_id=paper_id,
        limit=top_k,
        source=source
    )

    return data


@recommend_router.get("/specter/{paper_id}")
async def get_embedding_recommendation_for_paper(
        paper_id: str, top_k: int = 10
):
    data = await get_papers_with_embedding(
        paper_id=paper_id,
        top_k=top_k
    )

    return data
