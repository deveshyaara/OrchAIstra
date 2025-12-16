from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from . import config

embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL, google_api_key=config.GOOGLE_API_KEY)

# Ensure collection exists
try:
    client.get_collection(collection_name)
except:
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

vector_store = QdrantVectorStore(
    client=client, 
    collection_name=collection_name, 
    embedding=embeddings
)

def seed_knowledge_base():
    texts = [
        "Internal Strategy 2025: Molecule X shows promise for lung tissue regeneration.",
        "Clinical Note: Competitor Drug Y has high toxicity, leaving a gap in the market.",
        "Budget Memo: We have allocated $5M for repurposing existing assets."
    ]
    vector_store.add_texts(texts)
    print("[Qdrant] Knowledge Base Seeded in Cloud.")

def search_internal_docs(query: str):
    docs = vector_store.similarity_search(query, k=1)
    if not docs: return "No relevant internal records found."
    
    # Simple logic: If similarity is very high, it might be a cached report
    # For now, we return the content.
    return docs[0].page_content

def store_report(query: str, report_content: str):
    """Stores a generated report in the vector DB for future retrieval."""
    text = f"CACHED REPORT [Query: {query}]\n\n{report_content}"
    vector_store.add_texts([text])
    print(f"[Qdrant] Cached report for query: {query}")

def check_cache(query: str):
    """Checks if a report already exists for this query."""
    docs = vector_store.similarity_search_with_score(f"CACHED REPORT [Query: {query}]", k=1)
    if not docs: return None
    
    doc, score = docs[0]
    # If the semantic score is high enough (0.85+ indicates nearly identical intent), return it
    if score > 0.85: 
        print(f"[Internal] Cache Hit! Score: {score}")
        return doc.page_content
    return None