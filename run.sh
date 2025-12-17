#!/bin/bash
echo "🛑 Aggressively cleaning ports 8000-8081..."
lsof -t -i:8000 | xargs kill -9 2>/dev/null
lsof -t -i:8080 | xargs kill -9 2>/dev/null
lsof -t -i:8081 | xargs kill -9 2>/dev/null

echo "✅ Ports Cleared."
echo "🚀 Starting Jovian AI Server (Dev Mode - Port 8080)..."

# Run Python directly for better visibility
"/Users/adityasingh/agentic workflow/.env/bin/python" server.py 
