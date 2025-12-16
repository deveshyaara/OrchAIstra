from flask import Flask, render_template, request, Response, stream_with_context
import json
import time
from src.graph import build_graph
from src import vectors
from langchain_core.messages import HumanMessage

app = Flask(__name__)

# Initialize Knowledge Base once
vectors.seed_knowledge_base()
workflow = build_graph()

def generate_events(user_query):
    """
    Generator that runs the graph and yields JSON blocks for the frontend.
    """
    # Initial Yield to confirm connection
    yield json.dumps({"log": "> [System] Connection Established. Starting Engine...", "active_node": "master"}) + "\n"
    
    # State initialization
    initial_state = {"user_query": user_query, "plan": [], "results": []}
    
    try:
        # Stream events from LangGraph
        # We assume workflow.stream(state) yields intermediate steps
        events = workflow.stream(initial_state, config={"recursion_limit": 50})
        
        for event in events:
            for node, state in event.items():
                if node == "__end__": continue
                if state is None: continue # Skip if node returned no state update
                
                # Determine log message and active node based on graph event
                log_msg = ""
                active = node
                
                if node == "master":
                    # Check if master is delegating
                    plan = state.get("plan", [])
                    pending = [t for t in plan if t['status'] == 'pending']
                    if pending:
                        next_worker = pending[0]['worker_type']
                        log_msg = f"> [Master] Strategy Updated. Assigning task to [{next_worker.upper()}]."
                    else:
                         log_msg = "> [Master] Analyzing results & planning next steps..."
                         
                elif node in ["clinical", "patent", "web", "internal", "iqvia", "exim"]:
                    # Worker node finished
                    results = state.get("results", [])
                    if results:
                        last_res = results[-1]
                        summary = last_res.get("content", "")[:50] + "..."
                        log_msg = f"> [{node.upper()}] Task Complete. Data: {summary}"
                
                elif node == "report_gen":
                    log_msg = "> [Report] Compiling Final PDF Document..."
                
                if log_msg:
                    data = {"log": log_msg, "active_node": active}
                    yield json.dumps(data) + "\n"
                    # Small delay to allow UI animation to be visible
                    time.sleep(0.5) 
                    
        yield json.dumps({"log": "> [System] Workflow Finished.", "active_node": "report_gen"}) + "\n"
        
    except Exception as e:
        yield json.dumps({"log": f"> [Error] System Exception: {str(e)}", "active_node": "master"}) + "\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/run', methods=['POST'])
def run_analysis():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return {"error": "No query provided"}, 400

    return Response(stream_with_context(generate_events(query)), mimetype='application/x-ndjson')

@app.route('/api/download_report')
def download_report():
    try:
        # The agent saves to "Strategy_Report.pdf" in the CWD
        from flask import send_file
        return send_file("Strategy_Report.pdf", as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 404

if __name__ == '__main__':
    print("Starting Jovian AI Server (v2.1 - Patched) on port 8081...")
    # We use gunicorn for prod, but this is for local flask debug if needed
    app.run(debug=True, port=8081)
