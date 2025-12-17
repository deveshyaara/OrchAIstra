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
                    # Worker node finished - send full content, frontend will handle display
                    results = state.get("results", [])
                    if results:
                        last_res = results[-1]
                        full_content = last_res.get("content", "")
                        log_msg = f"> [{node.upper()}] Task Complete. Data: {full_content}"
                
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

@app.route('/api/help', methods=['POST'])
def help_chatbot():
    """AI assistant to help users understand how to use the system."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from src import config
        
        data = request.json
        question = data.get('question', '')
        
        # Create a specialized prompt for the help assistant
        system_prompt = """You are a helpful AI assistant for the Pharmaceutical R&D Research Assistant system.
        
Your role is to help users understand how to use this system effectively. The system:
- Analyzes pharmaceutical research opportunities
- Uses AI agents (Clinical, Patent, Web, Internal) to gather data
- Generates comprehensive PDF reports
- Supports queries like: "Investigate repurposing [drug] for [condition]"

Key features:
- Clinical Trials: Searches ClinicalTrials.gov
- Patent Analysis: Checks IP landscape and freedom-to-operate
- Web Intelligence: Finds market insights
- Report Generation: Creates professional PDFs with borders and formatting

Answer user questions concisely and helpfully. If they ask how to write queries, suggest formats like:
"Evaluate the potential of [drug name] for treating [condition]"
"What is the freedom-to-operate risk for [technology]?"
"Analyze the commercial viability of [drug/therapy]"

Keep responses under 100 words and friendly."""

        llm = ChatGoogleGenerativeAI(model=config.GEMINI_MODEL, temperature=0.5)
        response = llm.invoke(f"{system_prompt}\n\nUser Question: {question}")
        
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"I'm having trouble right now. Error: {str(e)}"}, 500

if __name__ == '__main__':
    print("Starting Jovian AI Server (v2.1 - Patched) on port 8080...")
    # Using Flask Dev Server for better error visibility
    app.run(debug=True, port=8080, host='0.0.0.0')
