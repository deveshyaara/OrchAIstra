from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict):
    user_query: str
    plan: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
