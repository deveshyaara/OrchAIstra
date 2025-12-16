#!/bin/bash
echo "🛑 Aggressively cleaning ports 8000-8081..."
lsof -t -i:8000 | xargs kill -9 2>/dev/null
lsof -t -i:8080 | xargs kill -9 2>/dev/null
lsof -t -i:8081 | xargs kill -9 2>/dev/null

echo "✅ Ports Cleared."
echo "🚀 Starting Jovian AI Server (Port 8080)..."

# Fallback to simple python if Gunicorn is trouble locally, but let's try Gunicorn one last time on standard 8080
"/Users/adityasingh/agentic workflow/.env/bin/gunicorn" --worker-class gthread --threads 4 --timeout 120 -b 0.0.0.0:8080 server:app 
