from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from . import config


embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL, google_api_key=config.GOOGLE_API_KEY)

# Init Qdrant Client (with error handling for network issues)
try:
    client = QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
    )
    collection_name = "pharma_internal_docs"

    # Ensure collection exists
    try:
        client.get_collection(collection_name)
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    print("[Qdrant] Connected successfully.")
except Exception as e:
    print(f"[Qdrant] WARNING: Could not connect to Qdrant ({e}). Vector features disabled.")
    client = None
    collection_name = None

# LAZY INITIALIZATION: Don't create vector_store at import time to avoid quota check
# This prevents the 429 error during server startup
vector_store = None

def _get_vector_store():
    """Lazy initialization of vector store to avoid startup quota checks."""
    global vector_store
    if vector_store is None:
        if client is None:
            raise Exception("Qdrant client not available")
        vector_store = QdrantVectorStore(
            client=client, 
            collection_name=collection_name, 
            embedding=embeddings
        )
    return vector_store


def seed_knowledge_base():
    texts = [
        "Internal Strategy 2025: Molecule X shows promise for lung tissue regeneration.",
        "Clinical Note: Competitor Drug Y has high toxicity, leaving a gap in the market.",
        "Budget Memo: We have allocated $5M for repurposing existing assets."
    ]
    try:
        _get_vector_store().add_texts(texts)
        print("[Qdrant] Knowledge Base Seeded in Cloud.")
    except Exception as e:
        print(f"[Qdrant] WARNING: Could not seed knowledge base: {e}")

def search_internal_docs(query: str):
    try:
        docs = _get_vector_store().similarity_search(query, k=1)
        if not docs: return "No relevant internal records found."
        return docs[0].page_content
    except Exception as e:
        print(f"[Qdrant] WARNING: Search failed: {e}")
        return "No relevant internal records found."

def store_report(query: str, report_content: str):
    """Stores a generated report in the vector DB for future retrieval."""
    try:
        text = f"CACHED REPORT [Query: {query}]\n\n{report_content}"
        _get_vector_store().add_texts([text])
        print(f"[Qdrant] Cached report for query: {query}")
    except Exception as e:
        print(f"[Qdrant] WARNING: Could not cache report: {e}")

def check_cache(query: str):
    """Checks if a report already exists for this query."""
    try:
        docs = _get_vector_store().similarity_search_with_score(f"CACHED REPORT [Query: {query}]", k=1)
        if not docs: return None
        
        doc, score = docs[0]
        # If the semantic score is high enough (0.85+ indicates nearly identical intent), return it
        if score > 0.85: 
            print(f"[Internal] Cache Hit! Score: {score}")
            return doc.page_content
        return None
    except Exception as e:
        print(f"[Qdrant] WARNING: Cache check failed: {e}")
        return None