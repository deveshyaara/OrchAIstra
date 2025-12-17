import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from . import config
from .state import AgentState
from . import tools
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_community.llms import FakeListLLM
import json

llm = ChatGoogleGenerativeAI(model=config.GEMINI_MODEL, temperature=0.3)

class PlanSchema(BaseModel):
    tasks: list[dict] = Field(description="List of tasks. Each task has 'worker_type', 'description', and 'parameters' (dict).")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def invoke_llm(prompt):
    return llm.invoke(prompt)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def invoke_structured_llm(prompt, schema):
    # We use a standard invoke and then parse, or use the structured method with a simpler prompt
    # Using the .with_structured_output method is generally reliable if the model supports it.
    # Gemini 2.0 Flash is good, but let's make the prompt very clear.
    structured_llm = llm.with_structured_output(schema)
    return structured_llm.invoke(prompt)

from . import vectors

def master_node(state: AgentState):
    print(f"\n[Master] Planning Step...")
    
    # 1. Check if we already have a finished plan
    if state.get("plan") and all(t['status'] == 'complete' for t in state['plan']):
        return {"final_report_path": "READY"}

    # 2. Check Cache (Optimization)
    if not state.get("plan"):
        cached_result = vectors.check_cache(state['user_query'])
        if cached_result:
            print(f"[Master] Found valid cached report. Skipping agents.")
            return {
                "results": [{"worker_id": "cache", "content": cached_result}],
                "plan": [{"task_id": "cache_hit", "worker_type": "report_gen", "status": "complete", "description": "Retrieved from Cache"}]
            }

    # 3. Create Plan (if no cache)
    if not state.get("plan"):
        # Explicitly ask for JSON to help the model
        prompt = f"""
You are a Master Strategist for Pharma R&D. Your task is to create a strategic plan to answer the following user query:
{state['user_query']}

You MAY use the following tools (agents):
- Clinical Trial Search (worker_type: 'clinical') - Parameters: molecule, condition
- Patent Analysis (worker_type: 'patent') - Parameters: molecule
- Web Intelligence (worker_type: 'web') - Parameters: query (free-form search)

Return a list of tasks in JSON format. Each task must have:
- worker_type: one of 'clinical', 'patent', 'web'
- description: what this agent will do
- parameters: a dictionary of parameters to pass to the tool

Example output:
{{"tasks": [
    {{"worker_type": "clinical", "description": "Search trials for thalidomide + leprosy", "parameters": {{"molecule": "thalidomide", "condition": "leprosy"}}}},
    {{"worker_type": "patent", "description": "Analyze IP for thalidomide", "parameters": {{"molecule": "thalidomide"}}}},
    {{"worker_type": "web", "description": "Find market data for thalidomide leprosy", "parameters": {{"query": "thalidomide leprosy market size"}}}}
]}}
"""
        
        try:
            print(f"[Master] 🧠 Invoking Thinking Model...")
            response = invoke_structured_llm(prompt, PlanSchema)
            
            # For thinking models, let's log the raw response if available
            if hasattr(response, 'thinking'):
                print(f"[Master] 💭 CHAIN OF THOUGHT:")
                print(f"    {response.thinking}")
            
            tasks = response.tasks
            print(f"[Master] ✅ Generated {len(tasks)} tasks")
        except Exception as e:
            # Fallback plan if LLM fails
            print(f"LLM Planning Failed: {e}. Using fallback plan.")
            class FallbackPlan:
                tasks = [
                    {"worker_type": "clinical", "description": "Search for clinical trials", "parameters": {"molecule": "Molecule X", "condition": "COPD"}},
                    {"worker_type": "patent", "description": "Analyze patent landscape", "parameters": {"molecule": "Molecule X"}},
                    {"worker_type": "web", "description": "Search for market news", "parameters": {"query": "Pharma market news"}}
                ]
            response = FallbackPlan()
            tasks = response.tasks
        
        new_tasks = []
        for t in tasks:
            # Handle both dict (if fallback) and object (if Pydantic)
            if isinstance(t, dict):
                w_type = t['worker_type']
                desc = t['description']
                params = t.get('parameters', {"q": state['user_query']})
            else:
                w_type = t.worker_type
                desc = t.description
                params = t.parameters # Pydantic model access
                
            new_tasks.append({
                "task_id": str(uuid.uuid4())[:8],
                "worker_type": w_type,
                "description": desc,
                "params": params, 
                "status": "pending"
            })
        
        new_tasks.append({"task_id": "end", "worker_type": "report_gen", "description": "PDF", "params": {}, "status": "pending"})
        return {"plan": new_tasks}
    
    return {}

def run_worker(state: AgentState, worker_name: str, tool_func):
    tasks = [t for t in state['plan'] if t['worker_type'] == worker_name and t['status'] == 'pending']
    if not tasks: return {}

    results = []
    # Create a copy of the full plan to update
    full_plan = [t.copy() for t in state['plan']]
    
    for task in tasks:
        try:
            params = task.get('params', {})
            
            if worker_name == "clinical": 
                # Ensure we have molecule and condition
                mol = params.get("molecule", "Unknown Molecule")
                cond = params.get("condition", "General")
                output = tool_func.invoke({"molecule": mol, "condition": cond})
            elif worker_name == "patent": 
                mol = params.get("molecule", "Unknown Molecule")
                output = tool_func.invoke({"molecule": mol})
            elif worker_name == "web":
                query = params.get("query", params.get("q", "Pharma trends"))
                output = tool_func.invoke({"query": query})
            elif worker_name == "internal":
                query = params.get("query", params.get("q", "Analysis"))
                output = tool_func.invoke({"query": query})
            elif worker_name == "report_gen":
                evidence = "\n".join([f"{r['worker_id']}: {r['content']}" for r in state['results']])
                try:
                    summary = invoke_llm(f"Summarize for Pharma Exec: {evidence}").content
                except Exception as e:
                    print(f"Report Gen LLM Failed: {e}")
                    summary = f"Executive Summary (Auto-Generated Fallback):\n\nBased on the collected evidence:\n{evidence}\n\n(Note: AI Summarization encountered an error, raw data provided above.)"
                
                # CACHE THE SUCCESSFUL REPORT
                print("[Report Agent] Caching result to Vector DB...")
                vectors.store_report(state['user_query'], summary)
                
                output = tool_func.invoke({"text": summary, "filename": "Strategy_Report.pdf"})
            else: 
                # Generic fallback 
                query = params.get("query", params.get("q", "Analysis"))
                # Try invoking with simple string if unknown tool signature, or dict if known
                try:
                    output = tool_func.invoke(query)
                except:
                    output = tool_func.invoke({"query": query})
        except Exception as e: output = str(e)

        results.append({"task_id": task['task_id'], "worker_id": worker_name, "content": str(output), "raw_data": output})
        
        # Update the specific task in the full plan
        for t in full_plan:
            if t['task_id'] == task['task_id']:
                t['status'] = 'complete'
                break
    
    # Append new results to existing results
    existing_results = state.get('results', [])
    new_results = existing_results + results
    
    return {"results": new_results, "plan": full_plan}