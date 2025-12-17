# Pharmaceutical R&D Research Assistant

## Overview
An AI-powered autonomous agent system that analyzes pharmaceutical research opportunities using multi-agent orchestration. The application investigates drug repurposing, patent landscapes, clinical trials, and market intelligence to generate comprehensive strategic reports.

## Core Functionality

### What It Does
- **Drug Repurposing Analysis**: Evaluates potential for existing drugs in new therapeutic areas
- **IP Landscape Assessment**: Analyzes patent status and freedom-to-operate risks
- **Clinical Trial Intelligence**: Searches ClinicalTrials.gov for relevant studies
- **Market Research**: Gathers competitive intelligence and market data
- **Report Generation**: Creates professional PDF reports with research findings

### How It Works
1. User submits research query (e.g., "Evaluate Thalidomide for leprosy reactions")
2. Master Agent plans task distribution across specialized worker agents
3. Specialized agents execute in parallel:
   - **CLINICAL**: ClinicalTrials.gov API searches
   - **PATENT**: PatentsView + ScrapingDog patent analysis
   - **WEB**: Google Search API + Gemini fallback
   - **INTERNAL**: Qdrant vector search (optional caching)
4. Report Generator compiles findings into formatted PDF
5. User downloads professional report with all research data

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **AI Orchestration**: LangGraph (state machine for agent workflow)
- **LLM**: Google Gemini 2.5-flash (latest model, Dec 2024)
- **Embeddings**: Google Generative AI Embeddings (models/embedding-001)
- **Vector Database**: Qdrant Cloud (semantic caching)
- **PDF Generation**: ReportLab (professional research paper formatting)
- **HTTP Client**: requests, httpx

### Frontend
- **UI Framework**: Vanilla HTML/CSS/JavaScript
- **Theme**: Black Dashboard (dark theme with pink/purple gradients)
- **Graph Visualization**: Cytoscape.js (network topology)
- **Streaming**: Server-Sent Events (SSE) via fetch API
- **Animations**: CSS transitions + JavaScript DOM manipulation

### AI & APIs
- **Primary LLM**: Gemini 2.5-flash (`gemini-2.5-flash`)
- **Clinical Data**: ClinicalTrials.gov API v2
- **Patent Data**: 
  - PatentsView API (granted patents & applications)
  - ScrapingDog Patent API (detailed analysis)
- **Web Search**: Google Custom Search API
- **Monitoring**: LangSmith (agent execution tracing)

### Infrastructure
- **Server**: Flask Development Server (local) or Gunicorn (production)
- **Port**: 8080
- **Deployment**: Docker + Render/Railway ready
- **Environment**: Python 3.12, virtual environment

## Architecture

### Agent System (LangGraph)
```
User Query
    ↓
Master Node (Planning)
    ↓
Worker Nodes (Parallel Execution)
    ├─ Clinical Agent
    ├─ Patent Agent
    ├─ Web Agent
    └─ Internal Agent
    ↓
Report Generator
    ↓
PDF Download
```

### File Structure
```
agentic workflow/
├── server.py                 # Flask app + streaming endpoints
├── run.sh                    # Server startup script
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── src/
│   ├── config.py            # API keys + model configuration
│   ├── agents.py            # Master + worker agent logic
│   ├── graph.py             # LangGraph workflow definition
│   ├── tools.py             # API integrations (Clinical, Patent, Web)
│   ├── vectors.py           # Qdrant vector store (caching)
│   └── state.py             # Agent state management
├── templates/
│   └── index.html           # Frontend UI (Black Dashboard theme)
└── deployment/
    ├── DEPLOY_GUIDE.md      # Render/Railway deployment
    ├── VERCEL_README.md     # Vercel deployment (limited)
    └── Procfile             # PaaS configuration
```

## Key Features

### 1. Multi-Agent Orchestration
- **Master Agent**: Uses Gemini 2.5 to plan task distribution
- **Worker Agents**: Specialized tools for different data sources
- **State Management**: LangGraph maintains workflow state
- **Parallel Execution**: Agents run concurrently for speed

### 2. Real-Time UI
- **Live Progress Tracking**: Streaming log updates
- **Network Visualization**: Animated graph showing active agents
- **Expandable Logs**: "Read More" for long responses (200+ chars)
- **Dark Theme**: Professional Black Dashboard aesthetics

### 3. Professional PDF Reports
- **Research Paper Formatting**: 1.25" margins, borders, headers/footers
- **Structured Content**: Title page, headings, justified text
- **Color Coding**: Pink headers (#e14eca), blue subheadings (#1d8cf8)
- **Metadata**: Page numbers, generation timestamp, confidentiality notice

### 4. Graph Visualization
- **Cytoscape.js**: Interactive network topology
- **Node Highlighting**: Active agent glows green during execution
- **Edge Animation**: Lines light up to show data flow
- **Screenshot Export**: Download graph as high-res PNG (2x scale)

### 5. AI Help Chatbot
- **Floating Bubble**: Bottom-right corner with gradient effect
- **Auto-Hiding Tooltip**: "Need help?" appears for 3 seconds
- **Gemini-Powered**: Uses same LLM for contextual help
- **Suggested Questions**: Pre-populated common queries

### 6. Semantic Caching (Optional)
- **Vector Store**: Qdrant Cloud for embedding storage
- **Cache Detection**: Checks for similar previous queries (>0.85 similarity)
- **Instant Results**: Returns cached reports for duplicate queries
- **Graceful Degradation**: Works without embeddings if quota exhausted

## API Integrations

| Service | Purpose | Status |
|---------|---------|--------|
| Google Gemini 2.5 | Primary LLM for planning/generation | ✅ Active |
| ClinicalTrials.gov | Clinical trial data | ✅ Active |
| PatentsView | Patent searches | ⚠️ Deprecated (fallback handling) |
| ScrapingDog | Enhanced patent details | ✅ Active |
| Google Search API | Market intelligence | ✅ Active |
| Qdrant Cloud | Vector database | ✅ Active (optional) |
| LangSmith | Agent monitoring | ✅ Active |

## Configuration

### Environment Variables
```bash
GOOGLE_API_KEY=AIzaSy...            # Gemini API key
GOOGLE_CSE_ID=855e2d7a464814fa4    # Custom Search Engine ID
QDRANT_URL=https://...             # Qdrant Cloud endpoint
QDRANT_API_KEY=eyJhbG...           # Qdrant authentication
GEMINI_MODEL=gemini-2.5-flash      # LLM model
EMBEDDING_MODEL=models/embedding-001
LANGCHAIN_API_KEY=lsv2_pt...       # LangSmith tracing
SCRAPINGDOG_API_KEY=6941a8f...     # Patent API
```

### Model Configuration
- **Current Model**: `gemini-2.5-flash` (latest, Dec 2024)
- **Temperature**: 0.3 (planning), 0.5 (chatbot)
- **Retry Logic**: 3 attempts with exponential backoff
- **Timeout**: 120 seconds per request

## Deployment

### Local Development
```bash
# Activate virtual environment
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
./run.sh
# Access at http://localhost:8080
```

### Docker Deployment
```bash
docker build -t pharma-research-assistant .
docker run -p 8080:8080 --env-file .env pharma-research-assistant
```

### Cloud Platforms
- **Render/Railway**: Full support (recommended)
- **Vercel**: Limited (10-60s timeout issues for long queries)
- **See**: `DEPLOY_GUIDE.md` for detailed instructions

## Performance

- **Query Processing**: 30-60 seconds for full analysis (3-4 agents)
- **API Calls**: ~5-10 per query (LLM, ClinicalTrials, Patents, Web)
- **PDF Generation**: <2 seconds
- **Vector Search**: <500ms (when enabled)

## Limitations

- **Embedding Quota**: Current API key has 0 quota (caching disabled)
- **PatentsView API**: Deprecated/unreliable (ScrapingDog compensates)
- **Gemini Thinking Model**: Not available (using 2.5-flash instead)
- **Vercel Timeout**: 10-60s limits prevent deployment there

## Sample Queries

```
1. "Evaluate the potential of Thalidomide for treating leprosy reactions"
2. "What is the freedom-to-operate risk for developing a new mRNA vaccine platform?"
3. "Analyze the commercial viability of GLP-1 receptor agonists for weight loss"
4. "Should we invest in CRISPR-Cas9 for sickle cell anemia?"
```

## Security & Best Practices

- **API Keys**: Stored in `src/config.py` (should use env vars for production)
- **Error Handling**: Try-except blocks with graceful fallbacks
- **Rate Limiting**: Retry logic with exponential backoff
- **Lazy Loading**: Vector store initialized only when needed
- **CORS**: Open (restrict for production deployment)

## Future Improvements

1. **Environment Variables**: Move all keys to `.env` file
2. **Paid Embedding Tier**: Enable semantic caching
3. **Google Patents Direct**: Replace unreliable PatentsView
4. **Streaming PDFs**: Generate report sections as agents complete
5. **User Authentication**: Add login for enterprise deployment
6. **Query History**: Save past searches with timestamps
7. **Export Options**: CSV, JSON, Word formats

---

**Version**: 2.1 (Patched)  
**Last Updated**: December 2024  
**License**: Internal Use  
**Contact**: For API quota increases or deployment support
