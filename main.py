import argparse
import sys
from src.graph import build_graph
import src.vectors as vectors

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the Agentic Pharma R&D Workflow.",
        epilog="Example: python main.py 'Develop strategy for repurposing Molecule X for COPD.'"
    )
    
    parser.add_argument(
        "query", 
        type=str, 
        help="The strategic research query for the Master Agent to process."
    )
    
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        parse_arguments().print_help()
        sys.exit(0)

    args = parse_arguments()
    user_query = args.query 
    
    vectors.seed_knowledge_base()
    app = build_graph()
    
    print(f"\nStarting Agentic AI Engine...")
    print(f"Query: {user_query}")
    
    result = app.invoke({"user_query": user_query, "plan": [], "results": []})
    
    print("\n" + "="*40)
    print("FINAL STRATEGIC REPORT")
    print("="*40)
    
    final_report_content = result.get('results', [])[-1].get('content', 'Report generation failed.')
    print(final_report_content)