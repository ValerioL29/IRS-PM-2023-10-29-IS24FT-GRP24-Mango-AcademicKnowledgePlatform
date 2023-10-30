import numpy as np
from gensim.models import Word2Vec
from pymilvus import MilvusClient
from sklearn.preprocessing import StandardScaler
from towhee import ops, pipe

from mango_server.config import milvus_config
from mango_server.db.core import get_paper_details

# Forming Searching Pipeline
# 1. Connect to Milvus server
milvus_client = ops.ann_search.milvus_client(
    uri=milvus_config['endpoint'],
    token=milvus_config['token'],
    collection_name=milvus_config['collection'],
    output_fields=['paper_id', 'title', 'year'],
    metric_type=milvus_config['metric_type'],
    limit=milvus_config['top_k']
)

# 2. Define the pipeline
# noinspection PyTypeChecker
search_pipe = pipe.input('query') \
    .map('query', 'vec', ops.text_embedding.dpr(model_name="facebook/dpr-ctx_encoder-single-nq-base")) \
    .map('vec', 'vec', lambda x: x / np.linalg.norm(x, axis=0)) \
    .flat_map('vec', ('id', 'score', 'paper_id', 'title', 'year'), milvus_client) \
    .output('query', 'id', 'score', 'paper_id', 'title', 'year')


def text_to_vector(text: str, word2vec: Word2Vec):
    text = text.lower()
    words = text.split()
    sentence_vec = [word2vec.wv[word] for word in words if word in word2vec.wv.index_to_key]
    vectors = np.ones((1, 768), dtype=np.float32) if not sentence_vec else sum(sentence_vec)

    return 10 * vectors / len(vectors)


async def search_on_milvus(vector) -> list:
    # Connect to Milvus server
    client = MilvusClient(
        uri=milvus_config['endpoint'],  # Cluster endpoint obtained from the cloud
        token=milvus_config['token']  # Token generated from the cloud
    )
    # Perform ANN search on Milvus cloud
    res = client.search(
        collection_name="testpaper",
        data=[vector],
        output_fields=["paper_id"]
    )

    return res


async def vector_search_with_gensim_word2vec(search_token: str):
    """Vector Search for Paper with Gensim Word2Vec"""
    # Load Word2Vec model for vectorization
    model = Word2Vec.load("models/word2vec.model")
    vectors = [model.wv[word] for word in model.wv.index_to_key]

    scaler = StandardScaler()
    scaled_vectors = scaler.fit_transform(vectors)

    for word, vector in zip(model.wv.index_to_key, scaled_vectors):
        model.wv[word] = vector

    # Search token from the frontend
    vector = text_to_vector(text=search_token, word2vec=model)
    res = await search_on_milvus(vector)

    # Fetch paper details from database
    paper_corpus_ids = [str(paper['entity']['paper_id']) for paper in res[0]]
    results = await get_paper_details(
        paper_ids=paper_corpus_ids,
        id_type="paperId",
    )

    return results


async def vector_search_with_towhee_pipeline(search_token: str,):
    """Vector Search for Paper with Towhee Pipeline"""
    # Search token with Towhee pipeline
    raw_ret = search_pipe(search_token).to_list()
    # Post-processing
    fields_list = ["query", "id", "score", "paper_id", "title", "year"]
    ret = [
        {
            field: elem[i]
            for i, field in enumerate(fields_list)
        }
        for elem in raw_ret
    ]
    paper_ids = [paper['paper_id'] for paper in ret]
    # Fetch paper details from database
    results = await get_paper_details(
        paper_ids=paper_ids
    )

    return results
