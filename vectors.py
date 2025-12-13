from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_core.embeddings import FakeEmbeddings
import config

embeddings = FakeEmbeddings(size=768)

client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
)

collection_name = "pharma_internal_docs"
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
    return docs[0].page_content if docs else "No relevant internal records found."