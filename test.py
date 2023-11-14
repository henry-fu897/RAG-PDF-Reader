"""
redis-embedder.py

What it does:
Read text from a pdf using PyPDF langchain integration
Download an embedding model from huggingface to deal with embeddings
Embed the documents into the redis server

"""


import os
import getpass

from typing import List

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.vectorstores.redis import Redis
from langchain.docstore.document import Document

from redisvl.index import SearchIndex

EMBEDDINGS = HuggingFaceEmbeddings()
INDEX_NAME = "pathfinder2erules"
REDIS_URL = "redis://192.168.1.250:6379"

def read_pdfs() -> List[Document]:
    print("[info.test]: Loading PDF Data...")
    loader = PyPDFLoader("pdf_data\\Pathfinder2ERulebook.pdf")
    pages = loader.load_and_split()
    print("[info.test]: Finished loading PDF Data, starting embedding process...")
    return pages


def redis_embed_documents (
        index_name: str,
        documents: List[Document],
        redis_url: str = "redis://192.168.1.250:6379"
    ):

    rds = Redis.from_documents(
        documents,
        EMBEDDINGS,
        redis_url=redis_url,
        index_name=index_name,
    )

    rds.write_schema("gen_schema.yaml")
    print(rds.similarity_search("How many actions do you have per turn?"))

    
def redis_query_documents (
        query: str,
        index_name: str,
        schema: str,
        redis_url: str = "redis://192.168.1.250:6379",
    ):

    rds = Redis.from_existing_index (
        EMBEDDINGS,
        index_name = index_name,
        redis_url = redis_url,
        schema = schema
    )
    
    context: List[Document] = rds.similarity_search(query)


if __name__ == "__main__":

    index = SearchIndex("pathfinder2erules")
    index.connect("redis://192.168.1.250:6379")

    query = "How many actions do you have per turn?"

    if not index.exists():
        redis_embed_documents(query, 
                              INDEX_NAME, REDIS_URL, read_pdfs(), "gen_schema.yaml")

    # We know the index has something 
    redis_query_documents()    
    
    
    