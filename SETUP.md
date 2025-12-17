# Quick Start Guide

## Prerequisites
- Python 3.10+
- pip
- virtualenv

## Setup (5 minutes)

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd agentic-workflow
```

### 2. Create Virtual Environment
```bash
python3 -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
```bash
# Copy the template
cp src/config.py.example src/config.py

# Edit src/config.py and add your real API keys:
# - GOOGLE_API_KEY (from https://aistudio.google.com/)
# - GOOGLE_CSE_ID (from Google Custom Search)
# - QDRANT_URL and QDRANT_API_KEY (from https://cloud.qdrant.io/)
# - SCRAPINGDOG_API_KEY (from https://scrapingdog.com/)
# - LANGCHAIN_API_KEY (optional, from https://smith.langchain.com/)
```

### 5. Run Application
```bash
./run.sh
```

Visit: **http://localhost:8080**

## Required API Keys

| Service | Required? | Get It From |
|---------|-----------|-------------|
| Google Gemini API | ✅ Yes | https://aistudio.google.com/ |
| Google Custom Search | ✅ Yes | https://programmablesearchengine.google.com/ |
| Qdrant Cloud | ⚠️ Optional | https://cloud.qdrant.io/ |
| ScrapingDog | ⚠️ Optional | https://scrapingdog.com/ |
| LangSmith | ❌ Optional | https://smith.langchain.com/ |

**Minimum to run**: Google Gemini API + Google Custom Search

## Troubleshooting

**Port 8080 already in use?**
```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Or edit run.sh to use different port
```

**Module not found?**
```bash
# Make sure virtual environment is activated
source .env/bin/activate
pip install -r requirements.txt
```

**API key errors?**
- Check `src/config.py` has real values (no "your-api-key-here")
- Verify keys at provider dashboards
- Check API quotas haven't been exceeded

## Usage

1. Open http://localhost:8080
2. Enter research query (e.g., "Evaluate Thalidomide for leprosy reactions")
3. Click "🚀 Launch Swarm"
4. Watch real-time agent execution
5. Download PDF report or graph screenshot

## Deployment

See [`DEPLOY_GUIDE.md`](DEPLOY_GUIDE.md) for production deployment to:
- Docker
- Render
- Railway
- ~~Vercel~~ (not recommended - timeout issues)
