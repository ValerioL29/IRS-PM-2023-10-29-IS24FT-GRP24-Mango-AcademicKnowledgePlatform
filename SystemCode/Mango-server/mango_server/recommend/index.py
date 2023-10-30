import tensorflow as tf
import tensorflow_recommenders as tfrs

from mango_server.db.core import get_paper_details
from mango_server.recommend.model import get_dual_tower_model, candidate_ds

# Load model
model_save_path = "models/dual_tower_weights/dual_tower_bf_v4"
model = get_dual_tower_model(weights_path=model_save_path)

# Build Brute Force Index
bf_index = tfrs.layers.factorized_top_k.BruteForce(model.query_model)
candidates = tf.data.Dataset.zip(
    (
        candidate_ds.batch(100).map(lambda x: x["paperId"]),
        candidate_ds.batch(100).map(model.candidate_model)
    )
)
bf_index.index_from_dataset(candidates)


async def query_with_bf_index(raw_query: dict, top_k: int = 10):
    # Vectorize query
    query = {}
    for k, v in raw_query.items():
        query[k] = tf.constant([v])
    # Get top 10 results
    _, raw_paper_ids = bf_index(query, k=top_k)
    paper_ids = raw_paper_ids.numpy().reshape(-1).astype(str).tolist()
    # Get paper details
    paper_details = await get_paper_details(
        paper_ids=paper_ids
    )
    
    return paper_details
