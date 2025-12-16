# Deployment Guide: Agentic Research Assistant

This guide outlines how to deploy your application to **Render.com** (recommended for ease of use and free tier) using the files we've prepared.

## 1. Prerequisites
- A **GitHub Account**.
- A **Render.com Account** (connected to your GitHub).
- The project code pushed to a GitHub repository.

## 2. Steps to Deploy on Render

### Step A: Push Code to GitHub
Ensure all your files (`Dockerfile`, `requirements.txt`, `config.py`, `src/`, etc.) are committed and pushed to a new repo on GitHub.

### Step B: Create New Web Service in Render
1.  Log in to dashboard.render.com.
2.  Click **"New"** -> **"Web Service"**.
3.  Connect the GitHub repository you just created.

### Step C: Configure Service
- **Name**: `jovian-research-agent` (or similar)
- **Region**: Closest to you (e.g., Singapore, Frankfurt, Oregon).
- **Branch**: `main` (or `master`).
- **Runtime**: **Docker** (Select "Docker" as the runtime environment).
    - *Note: Since we have a `Dockerfile`, Render will automatically detect and use it.*
- **Instance Type**: Free (or Starter if you need more RAM).

### Step D: Environment Variables
You MUST add your secret keys. In the **"Environment"** or **"Advanced"** section, add the following key-value pairs:
- `GOOGLE_API_KEY`: `[Your Gemini Key]`
- `GOOGLE_CSE_ID`: `[Your Search Engine ID]`
- `QDRANT_URL`: `[Your Qdrant URL]`
- `QDRANT_API_KEY`: `[Your Qdrant Key]`
- `LANGCHAIN_TRACING_V2`: `true`
- `LANGCHAIN_API_KEY`: `[Your LangSmith Key]`
- `SCRAPINGDOG_API_KEY`: `6941a8f45e99eff20d233b2f`

### Step E: Deploy
1.  Click **"Create Web Service"**.
2.  Render will start building the Docker image. This may take 3-5 minutes.
3.  Once the build finishes, you will see `HostPort: 8080` in the logs.
4.  Your app will be live at `https://jovian-research-agent.onrender.com`!

## Alternative: Railway or Fly.io
Since we have a robust `Dockerfile`, you can also deploy to:
- **Railway**: `railway up` (automatically builds from Dockerfile).
- **Fly.io**: `fly launch` (generates fly.toml and deploys).

## Troubleshooting
- **Build Fails?**: Check the logs. Usually a missing dependency in `requirements.txt` (but we verified it).
- **App Crashes?**: Check environment variables. If `GOOGLE_API_KEY` is missing, the LLM will fail on startup.
