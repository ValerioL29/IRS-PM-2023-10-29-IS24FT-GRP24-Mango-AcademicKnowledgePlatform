from mango_server.utils.aiohttp_utils import post_request_with_body, get_request_with_query
from mango_server.config import S2_API_KEY, paper_detail_fields


async def get_paper_recommendation_with_pos_and_neg(
    pos_paper_ids: list[str],
    neg_paper_ids: list[str],
    top_k: int = 10
):
    """
    Get paper recommendation with positive and negative paper IDs.
    """
    url = "https://api.semanticscholar.org/recommendations/v1/papers/"
    body = {
      "positivePaperIds": pos_paper_ids,
      "negativePaperIds": neg_paper_ids
    }
    params = {
        "limit": top_k,
        "fields": ",".join(paper_detail_fields)
    }
    header = {
        "x-api-key": S2_API_KEY
    }
    # Get the results
    ret = await post_request_with_body(
        request_url=url,
        request_body=body,
        request_params=params,
        request_header=header
    )

    return ret


async def get_paper_recommendation_for_single_pos(
        paper_id: str,
        source: str = "recent",
        limit: int = 10
):
    """Get recommended papers for a single positive example paper"""
    url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}"
    ret = await get_request_with_query(
        request_url=url,
        request_query={
            "from": source,
            "limit": limit,
            "fields": ",".join(paper_detail_fields)
        }
    )

    return ret
