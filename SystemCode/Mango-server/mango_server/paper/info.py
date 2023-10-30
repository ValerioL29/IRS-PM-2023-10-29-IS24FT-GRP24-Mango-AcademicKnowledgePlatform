from mango_server.db.core import get_records_with_ids, get_paper_detail_with_id


async def get_single_paper_info_with_id(paper_id: str):
    """Fetch a single paper details with paper id"""
    return await get_paper_detail_with_id(
        paper_id=paper_id
    )


async def get_paper_details_in_batch_with_ids(paper_ids: list[str]):
    """Fetch a batch of paper details with paper ids"""
    return await get_records_with_ids(
        paper_ids=paper_ids
    )
