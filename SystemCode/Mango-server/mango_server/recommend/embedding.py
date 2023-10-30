from pymilvus import MilvusClient

from mango_server.config import milvus_config
from mango_server.db.core import get_paper_detail_with_id, get_records_with_ids

# Initialize a MilvusClient instance
# Replace uri and token with your own
client = MilvusClient(
    uri=milvus_config['endpoint'],
    token=milvus_config['token']
)


async def get_papers_with_embedding(paper_id: str, top_k: int = 10):
    """Get papers' ANN with its paper_id"""
    # Fetch paper embedding from DuckDB
    paper_data = await get_paper_detail_with_id(
        paper_id=paper_id,
        id_type="paper_id",
        table_name='paper_embedding',
        fields_list=['paper_id', 'vector'],
        db_path="stores/mango-profile.duckdb"
    )
    # Search paper embedding in Milvus
    paper_embedding = paper_data['vector']
    paper_ann_list = client.search(
        collection_name="papers",
        data=[paper_embedding],
        output_fields=["paper_id"],
        limit=top_k
    )[0]
    paper_ann_ids = [
        elem['entity']['paper_id']
        for elem in paper_ann_list
    ]
    # Return details of papers
    ret_details = await get_records_with_ids(
        paper_ids=paper_ann_ids
    )

    return ret_details
