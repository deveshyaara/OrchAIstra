import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import config
from state import AgentState
import tools
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_community.llms import FakeListLLM
import json

llm = ChatGoogleGenerativeAI(model=config.GEMINI_MODEL, temperature=0.3)

class PlanSchema(BaseModel):
    tasks: list[dict] = Field(description="List of tasks with 'worker_type' and 'description'.")

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

def master_node(state: AgentState):
    print(f"\n[Master] Planning Step...")
    
    if state.get("plan") and all(t['status'] == 'complete' for t in state['plan']):
        return {"final_report_path": "READY"}

    if not state.get("plan"):
        # Explicitly ask for JSON to help the model
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Pharma R&D Strategy Manager. Create a research plan. "
                       "Return a JSON object with a 'tasks' list. "
                       "Each task must have: 'worker_type' (one of: clinical, patent, web, internal, iqvia, exim) "
                       "and 'description' (string)."),
            ("human", f"Query: {state['user_query']}")
        ])
        
        try:
            plan = invoke_structured_llm(prompt, PlanSchema)
        except Exception as e:
            # Fallback plan if LLM fails
            print(f"LLM Planning Failed: {e}. Using fallback plan.")
            class FallbackPlan:
                tasks = [
                    {"worker_type": "clinical", "description": "Search for clinical trials"},
                    {"worker_type": "patent", "description": "Analyze patent landscape"},
                    {"worker_type": "web", "description": "Search for market news"}
                ]
            plan = FallbackPlan()
        
        new_tasks = []
        for t in plan.tasks:
            # Handle both dict (if fallback) and object (if Pydantic)
            if isinstance(t, dict):
                w_type = t['worker_type']
                desc = t['description']
            else:
                w_type = t.worker_type
                desc = t.description
                
            new_tasks.append({
                "task_id": str(uuid.uuid4())[:8],
                "worker_type": w_type,
                "description": desc,
                "params": {"q": state['user_query']}, 
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
            if worker_name == "clinical": output = tool_func.invoke({"molecule": "Molecule X", "condition": "COPD"})
            elif worker_name == "patent": output = tool_func.invoke("Molecule X")
            elif worker_name == "report_gen":
                evidence = "\n".join([f"{r['worker_id']}: {r['content']}" for r in state['results']])
                try:
                    summary = invoke_llm(f"Summarize for Pharma Exec: {evidence}").content
                except Exception as e:
                    print(f"Report Gen LLM Failed: {e}")
                    summary = f"Executive Summary (Auto-Generated Fallback):\n\nBased on the collected evidence:\n{evidence}\n\n(Note: AI Summarization encountered an error, raw data provided above.)"
                output = tool_func.invoke({"text": summary})
            else: output = tool_func.invoke(state['user_query'])
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