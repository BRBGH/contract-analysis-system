import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from typing import List, Dict, Any, Tuple
from config import CHROMA_DB_PATH, TOP_K_RESULTS, OPENAI_API_KEY
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def create_embeddings():
    """Create embedding model using OpenAI"""
    return OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model="text-embedding-3-small"
    )

def create_vector_store(chunks: List[Dict[str, Any]], COLLECTION_NAME = "default_collection") -> Chroma:
    """Create and populate or load existing vector store"""
    print("Checking for existing Chroma vector store...")

    # Create embeddings
    embeddings = create_embeddings()

    # Try to load existing Chroma DB
    if os.path.exists(CHROMA_DB_PATH) and os.path.isdir(CHROMA_DB_PATH):
        try:
            vector_store = Chroma(
                embedding_function=embeddings,
                persist_directory=CHROMA_DB_PATH,
                collection_name=COLLECTION_NAME
            )
            print("Loaded existing vector store.")
            return vector_store
        except Exception as e:
            print(f"Failed to load existing vector store: {e}")
            print("Creating new vector store...")

    # If not found or failed to load, create new store
    print("Creating new vector store...")
    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk['content'],
            metadata={
                'chunk_id': chunk['chunk_id'],
                'page_number': chunk['page_number'],
                'element_type': chunk.get('element_type', 'unknown')
            }
        )
        documents.append(doc)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH
    )

    print(f"Vector store created with {len(documents)} documents")
    return vector_store

def search_similar_chunks(vector_store: Chroma, query: str, k: int = TOP_K_RESULTS) -> List[Tuple[Document, float]]:
    """Search for similar chunks"""
    return vector_store.similarity_search_with_score(query, k=k)
