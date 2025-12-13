from langgraph.graph import StateGraph, END
from state import AgentState
from agents import master_node, run_worker
import tools

def node_clinical(s): return run_worker(s, "clinical", tools.tool_clinical_trials)
def node_patent(s): return run_worker(s, "patent", tools.tool_patents_view)
def node_web(s): return run_worker(s, "web", tools.tool_web_intel)
def node_internal(s): return run_worker(s, "internal", tools.tool_internal_rag)
def node_iqvia(s): return run_worker(s, "iqvia", tools.tool_iqvia_mock)
def node_exim(s): return run_worker(s, "exim", tools.tool_exim_mock)
def node_report(s): return run_worker(s, "report_gen", tools.tool_generate_pdf)

def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("master", master_node)
    workflow.add_node("clinical", node_clinical)
    workflow.add_node("patent", node_patent)
    workflow.add_node("web", node_web)
    workflow.add_node("internal", node_internal)
    workflow.add_node("iqvia", node_iqvia)
    workflow.add_node("exim", node_exim)
    workflow.add_node("report_gen", node_report)

    def router(state):
        if not state.get("plan"): return "master"
        pending = [t for t in state['plan'] if t['status'] == 'pending']
        if not pending: return END
        return pending[0]['worker_type']

    workflow.set_entry_point("master")
    
    workflow.add_conditional_edges("master", router, {
        "clinical": "clinical", "patent": "patent", "web": "web",
        "internal": "internal", "iqvia": "iqvia", "exim": "exim",
        "report_gen": "report_gen", END: END
    })

    for w in ["clinical", "patent", "web", "internal", "iqvia", "exim", "report_gen"]:
        workflow.add_edge(w, "master")

    return workflow.compile()