import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyAnJz5FL9KLLg10WMFKCn4zJ7PhE4ejlcI" 
os.environ["GOOGLE_CSE_ID"] = "855e2d7a464814fa4"

QDRANT_URL = "https://88cd8b21-0ead-4427-bbd3-ce95b729a414.us-east4-0.gcp.cloud.qdrant.io" 
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jAP768Wx9hQ5Cpp-UXu-jd0J1d8UYjRLFdmQMgi6tVw" 

# Switched to Thinking Model for Chain of Thought reasoning
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp-01-21"
EMBEDDING_MODEL = "models/embedding-001"

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "agentic-workflow-v2")

# Patent APIs
SCRAPINGDOG_API_KEY = "6941a8f45e99eff20d233b2f" # User provided key
