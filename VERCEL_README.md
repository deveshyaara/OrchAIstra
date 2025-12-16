# Vercel Deployment Guide

Deploying this Agentic Workflow to Vercel is possible but requires attention to **Function Timeouts**.

## 1. Timeout Warning ⚠️
Vercel Serverless Functions have a default timeout of **10 seconds** (Hobby Plan) or **60 seconds** (Pro Plan).
The full Agentic Workflow (Clinical -> Patent -> Web -> Report) often takes **>60 seconds**.
- **Result**: The request might time out before the report is finished on Vercel.
- **Recommended**: Use **Render** (via Docker) or **Railway** for long-running agents as described in `DEPLOY_GUIDE.md`.

## 2. Deploying to Vercel (If you still want to try)

### Option A: Vercel CLI
1.  Install Vercel CLI: `npm i -g vercel`
2.  Run `vercel` in this directory.
3.  Follow the prompts.

### Option B: Git Push
1.  Push this code to your GitHub repository.
2.  Go to **vercel.com/new**.
3.  Import your repository.
4.  **Environment Variables**: You MUST add these in Vercel Settings:
    - `GOOGLE_API_KEY`
    - `GOOGLE_CSE_ID`
    - `QDRANT_URL`
    - `QDRANT_API_KEY`
    - `LANGCHAIN_TRACING_V2`: `true`
    - `LANGCHAIN_API_KEY`
    - `SCRAPINGDOG_API_KEY`

## 3. Configuration Notes
- The `vercel.json` file is already configured to route all traffic to `server.py`.
- The `@vercel/python` runtime will automatically install dependencies from `requirements.txt`.
