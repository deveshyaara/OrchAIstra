import streamlit as st
import time
from graph import build_graph
import vectors
import os
import json

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Jovian AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. APPLE x GEMINI CSS SYSTEM ---
st.markdown("""
<style>
    /* 1. Global Typography & Reset */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, div {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #e0e0e0; /* Soft White */
        background-color: #121212; /* Soothing Matte Black */
    }

    /* 2. Clean Background (Matte Black) */
    .stApp {
        background-color: #121212;
    }

    /* 3. Glassmorphism Cards (Dark) */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* 4. Input Field (Dark & Visible) */
    .stTextInput>div>div>input {
        background: #262626; /* Dark Grey Input */
        color: #ffffff !important; /* White Text */
        border: 1px solid #404040;
        border-radius: 12px;
        padding: 16px;
        font-size: 16px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    .stTextInput>div>div>input:focus {
        border-color: #0071e3; /* Apple Blue */
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.2);
        background: #2b2b2b;
    }
    /* Placeholder Visibility Fix */
    .stTextInput input::placeholder {
        color: #aaaaaa !important;
        opacity: 1;
    }

    /* 5. Buttons (Apple Blue - High Contrast) */
    .stButton>button {
        background: #0071e3;
        color: white !important;
        border-radius: 980px; /* Pill shape */
        padding: 10px 24px;
        font-weight: 500;
        border: none;
        box-shadow: 0 2px 10px rgba(0, 113, 227, 0.3);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: #0077ed;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(0, 113, 227, 0.5);
    }

    /* 6. Typography Headers */
    h1 {
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%); /* White Gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h3 {
        font-weight: 600;
        color: #f5f5f7;
        margin-bottom: 16px;
    }

    /* 7. Status/Thinking Indicators (Dark Mode) */
    .thinking-step {
        padding: 12px 16px;
        margin: 8px 0;
        background: #1e1e1e;
        border-radius: 12px;
        border-left: 4px solid #0071e3;
        font-size: 14px;
        color: #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* 8. News Card (Dark Mode) */
    .news-card {
        background: #1e1e1e;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        border: 1px solid #333;
    }
    .news-source {
        font-size: 11px;
        text-transform: uppercase;
        color: #a1a1a6;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .news-title {
        font-size: 15px;
        font-weight: 600;
        color: #f5f5f7;
        margin-bottom: 8px;
    }
    .news-summary {
        font-size: 13px;
        color: #c7c7cc;
        line-height: 1.4;
    }

    /* 9. Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #121212; /* Match Main Background */
        border-right: 1px solid #333;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### Jovian AI")
    st.caption("Enterprise Intelligence v2.1")
    
    st.markdown("#### Neural Swarm")
    
    agents = [
        ("Master Orchestrator", "Strategy & Planning", "#0071e3"),
        ("Clinical Trials", "Safety & Efficacy", "#34c759"),
        ("Patent Landscape", "IP & FTO Analysis", "#af52de"),
        ("Web Intelligence", "Market Signals", "#ff9500"),
        ("Internal Knowledge", "Proprietary Data", "#ff2d55")
    ]
    
    for name, role, color in agents:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.1);">
            <div style="width: 10px; height: 10px; background: {color}; border-radius: 50%;"></div>
            <div>
                <div style="font-weight: 600; font-size: 13px; color: #f5f5f7;">{name}</div>
                <div style="font-size: 11px; color: #a1a1a6;">{role}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Clear Context"):
        with st.spinner("Resetting..."):
            vectors.seed_knowledge_base()
        st.toast("Memory cleared", icon="✨")

# --- 4. MAIN LAYOUT ---

# Hero Section
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063228.png", width=64)
with col_title:
    st.title("Research Assistant")
    st.markdown("Autonomous feasibility analysis for pharmaceutical R&D.")

st.markdown("---")

# Input Section
with st.container():
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        query = st.text_input(
            "Research Directive", 
            placeholder="Ask anything (e.g., 'Analyze Metformin for longevity')...",
            label_visibility="collapsed"
        )
    with col_btn:
        st.write("") # Spacer
        launch_btn = st.button("Generate", type="primary", use_container_width=True)

# --- 5. EXECUTION ENGINE ---
    # --- 5. EXECUTION ENGINE ---
    if launch_btn and query:
        
        # Layout: 2 Columns (Main Content | Sidebar-like Info)
        # We'll put the report in the center and "Thinking" in a collapsible
        
        st.divider()
        
        # 1. UNIFIED CHAIN OF THOUGHT (Gemini Style)
        # We use a single status container for the entire process
        with st.status("Thinking...", expanded=True) as status:
            st.markdown("Analyzing request...")
            
            # Initialize
            app = build_graph()
            history = []
            
            try:
                events = app.stream(
                    {"user_query": query, "plan": [], "results": []},
                    config={"recursion_limit": 50}
                )
                
                for event in events:
                    for node, state in event.items():
                        if node == "__end__": continue
                        if not state: continue
                        
                        # MASTER AGENT
                        if node == "master":
                            st.markdown(f"**Strategy:** Planning execution steps...")
                            if 'plan' in state:
                                for t in state['plan']:
                                    if t['status'] == 'pending':
                                        st.markdown(f"- ➜ Assigning **{t['worker_type'].title()}**")

                        # WORKER AGENTS
                        elif 'results' in state:
                            result = state['results'][-1]
                            worker = result['worker_id']
                            content = result['content']
                            
                            # Clean Names
                            name_map = {
                                "clinical": "Clinical Trials",
                                "patent": "Patent Landscape",
                                "web": "Web Intelligence",
                                "internal": "Internal Knowledge",
                                "report_gen": "Report Generator"
                            }
                            agent_name = name_map.get(worker, worker.title())
                            
                            st.markdown(f"**{agent_name}:** Task complete.")
                            
                            # If it's the patent tool and used fallback, mention it subtly
                            if worker == "patent" and "Synthetic" in content:
                                st.caption("Used Synthetic Intelligence (Patent API Deprecated)")

                        history.append(state)
                
                status.update(label="Thinking Complete", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"System Error: {e}")
                status.update(label="System Error", state="error")

        # 2. RESULTS DISPLAY
        # Once thinking is done (collapsed), show the results
        
        # Check for final report
        report_path = None
        for step in history:
            if 'results' in step:
                for r in step['results']:
                    if r['worker_id'] == "report_gen":
                        report_path = r['content']

        if report_path:
            st.markdown("### 📑 Strategic Report")
            
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="margin-top:0;">Executive Summary</h3>
                <p style="font-size: 14px; color: #424245;">
                    The autonomous swarm has successfully generated a comprehensive feasibility report for: <strong>{query}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display Intelligence Cards (News/Patents) in a Grid
            st.markdown("#### Intelligence Gathered")
            col_news1, col_news2 = st.columns(2)
            
            news_items = []
            for step in history:
                if 'results' in step:
                    res = step['results'][-1]
                    if res['worker_id'] in ["web", "patent", "clinical"]:
                        news_items.append(res)
            
            for i, item in enumerate(news_items):
                worker = item['worker_id']
                content = item['content']
                target_col = col_news1 if i % 2 == 0 else col_news2
                
                with target_col:
                    # Styling based on source
                    border_color = "#0071e3"
                    title = "Market Signal"
                    
                    # Defaults
                    badge_html = ""
                    
                    if worker == "patent": 
                        border_color = "#af52de"
                        title = "Patent Analysis"
                        
                        # PARSE RISK STATUS
                        import re
                        risk_match = re.search(r"Overall FTO Risk:\s*(HIGH|MEDIUM|LOW)", content, re.IGNORECASE)
                        if risk_match:
                            risk_level = risk_match.group(1).upper()
                            badge_color = "#ff3b30" # Red
                            if risk_level == "MEDIUM": badge_color = "#ff9500" # Orange
                            if risk_level == "LOW": badge_color = "#34c759" # Green
                            
                            badge_html = f"""
                            <span style="
                                background-color: {badge_color}; 
                                color: white; 
                                padding: 2px 8px; 
                                border-radius: 4px; 
                                font-size: 10px; 
                                font-weight: 700;
                                margin-left: 8px;
                                vertical-align: middle;
                            ">{risk_level} RISK</span>
                            """

                    elif worker == "clinical":
                        border_color = "#34c759"
                        title = "Clinical Data"
                        
                    # Clean up content for preview
                    preview_text = content[:200] + "..." if len(content) > 200 else content
                    
                    st.markdown(f"""
                    <div class="news-card" style="border-left: 4px solid {border_color};">
                        <div class="news-source" style="color: {border_color};">
                            {worker.upper()} {badge_html}
                        </div>
                        <div class="news-title">{title}</div>
                        <div class="news-summary">{preview_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Read More Expander
                    if len(content) > 200:
                        with st.expander("Read Full Details"):
                            st.markdown(content)

            # PDF Download
            st.markdown("---")
            if "PDF Saved successfully: " in report_path:
                clean_path = report_path.replace("PDF Saved successfully: ", "").strip()
                if os.path.exists(clean_path):
                    with open(clean_path, "rb") as f:
                        st.download_button(
                            "Download Full PDF Report", 
                            f, 
                            file_name="Strategy_Report.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                else:
                    st.warning("PDF file generated but not found on disk.")
        else:
            st.info("Analysis in progress or failed to generate report.")