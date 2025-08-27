import os

# OpenAI Configuration
OPENAI_API_KEY = "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"  # You'll set this in your environment
OPENAI_MODEL = "gpt-4o"  # Using GPT-4o as the default model
OPENAI_TEMPERATURE = 0.0

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "contract_chunks"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5

