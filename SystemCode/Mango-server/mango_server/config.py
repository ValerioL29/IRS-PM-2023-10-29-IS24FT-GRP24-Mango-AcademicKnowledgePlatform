import json
import logging
import sys

try:
    with open('config.json', 'r+', encoding='utf-8') as config_obj:
        application_conf: dict = json.load(config_obj)
except FileNotFoundError:
    logging.error("Please ensure 'config.json' exists.")
    raise sys.exit()

# Metastore stuff
METASTORE_URL = application_conf.get('metastore')

# Semantic Scholar stuff
S2_API_KEY = application_conf.get('api_key')

# Paper detail fields
paper_all_fields = [
    'paperId', 'corpusId', 'url', 'title',
    'venue', 'year', 'citationCount', 'isOpenAccess',
    'fieldsOfStudy', 's2FieldsOfStudy', 'tldr', 'embedding',
    'authors', 'id', 'code_links', 'details'
]
paper_detail_fields = list(
    set(paper_all_fields) - {'embedding', 's2FieldsOfStudy'}
)

# Vector search stuff
milvus_config = application_conf.get('milvus')
