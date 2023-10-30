from fastapi import APIRouter

from mango_server.search.ann import vector_search_with_gensim_word2vec, vector_search_with_towhee_pipeline

search_router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@search_router.post("/gensim")
async def search_paper_with_gensim(token: str):
    data = await vector_search_with_gensim_word2vec(search_token=token)

    return {
        "search_token": token,
        "papers": data
    }


@search_router.post("/towhee")
async def search_paper_with_towhee(token: str):
    data = await vector_search_with_towhee_pipeline(search_token=token)

    return {
        "search_token": token,
        "papers": data
    }
