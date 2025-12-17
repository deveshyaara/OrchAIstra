# Demo Walkthrough Script
## Pharmaceutical R&D Research Assistant

---

## Introduction (30 seconds)

"Welcome to the **Pharmaceutical R&D Research Assistant** - an AI-powered autonomous agent system built with **Google Gemini 2.5** and **LangGraph**. 

This application helps pharmaceutical researchers evaluate drug repurposing opportunities by orchestrating multiple specialized AI agents that search clinical trials, analyze patents, and gather market intelligence - all in real-time.

Let me walk you through a live example."

---

## Step 1: Interface Overview (15 seconds)

**[Point to screen]**

"Here's our interface using the **Black Dashboard** theme. On the left, we have a **real-time network topology graph** powered by **Cytoscape.js** that visualizes our agent system. On the right is the control panel with our input field and live progress logs."

---

## Step 2: Submit Research Query (20 seconds)

**[Type in input box]**

"Let's investigate a real-world drug repurposing scenario. I'll enter:"

> **"Evaluate the potential of Thalidomide for treating leprosy reactions"**

**[Point to input]**

"The system accepts natural language queries about drug repurposing, IP risks, clinical trials, or market analysis."

**[Click "🚀 Launch Swarm"]**

"Now I'll launch the agent swarm."

---

## Step 3: Real-Time Agent Execution (45 seconds)

**[As agents execute, narrate]**

"Watch the **live visualization** on the left:

**[Master node lights up - GREEN]**
- 'The **Master Agent** is using **Gemini 2.5-flash** to plan the research strategy. It's deciding which specialized agents to deploy.'

**[Clinical node lights up - GREEN, edges animate]**
- 'Now the **Clinical Agent** is searching **ClinicalTrials.gov API v2** for trials involving Thalidomide and leprosy.'

**[Patent node lights up - GREEN]**
- 'The **Patent Agent** is querying **PatentsView** and **ScrapingDog APIs** to analyze the IP landscape and freedom-to-operate risks.'

**[Web node lights up - GREEN]**
- 'The **Web Intelligence Agent** is using **Google Custom Search API** to gather market data and competitive intelligence.'

**[Point to logs on right]**

'On the right, you can see **streaming progress logs**. Each agent reports back with its findings in real-time. Notice the logs are **expandable** - for long responses, there's a \"Read More\" button to see full details.'

**[Report node lights up - GREEN]**
- 'Finally, all data flows to the **Report Generator**, which compiles everything into a professional PDF using **ReportLab**.'

---

## Step 4: Download & Review PDF Report (30 seconds)

**[Click "📄 Download PDF" button]**

"The workflow is complete. Let me download the generated report."

**[Open downloaded PDF]**

"Here's the strategic feasibility report. Notice the **professional formatting**:
- **Title page** with generation timestamp
- **Borders and margins** styled like an academic research paper  
- **Color-coded headers** - pink for main sections (#e14eca), blue for subsections (#1d8cf8)
- **Headers and footers** on every page with page numbers and confidentiality notice
- **Structured content** with clinical trial data, patent analysis, and market insights

This is generated entirely by the system using **ReportLab** with custom templates matching our Black Dashboard theme."

---

## Step 5: Download & Review Graph Visualization (25 seconds)

**[Click "📷 Screenshot Graph" button]**

"We can also export the network topology. Let me screenshot the agent graph."

**[Download completes, open PNG]**

"This is a **high-resolution PNG export** (2x scale) showing our multi-agent architecture:
- The **Master node** at the center coordinating everything
- **Worker nodes** (Clinical, Patent, Web, Internal) arranged around it
- **Report Generator** at the bottom collecting all results
- This visualization was generated using **Cytoscape.js** - the same library that powers biological network analysis

This graph helps stakeholders understand our AI orchestration architecture at a glance."

---

## Technical Highlights (30 seconds)

**[Optional - if time permits]**

"Let me highlight the technical stack:

**Backend:**
- **LangGraph** for multi-agent state management
- **Google Gemini 2.5-flash** (latest Dec 2024 model) for planning and synthesis
- **Flask with Server-Sent Events** for real-time streaming
- **Qdrant vector database** for semantic caching (optional)

**Frontend:**
- **Vanilla JavaScript** with custom streaming implementation
- **Cytoscape.js** for interactive graph visualization
- **Black Dashboard CSS theme** for professional dark UI

**APIs Integrated:**
- ClinicalTrials.gov, PatentsView, ScrapingDog, Google Search
- All orchestrated in parallel for 30-60 second total execution time"

---

## Advanced Features (20 seconds - Optional)

**[If demonstrating chatbot]**

"We've also included an **AI-powered help assistant** in the bottom right corner."

**[Click 💬 bubble]**

"This uses the same **Gemini model** to answer questions about how to use the system - though honestly, it's mostly for show since the interface is quite straightforward."

---

## Closing (15 seconds)

"In summary, this application demonstrates:
1. **Multi-agent orchestration** using LangGraph
2. **Real-time streaming** with animated visualizations  
3. **Professional report generation** with custom PDF formatting
4. **Production-ready architecture** deployable to Render, Railway, or Docker

The entire system processes complex pharmaceutical research queries in under a minute, providing researchers with comprehensive analysis across clinical, patent, and market dimensions."

---

## Q&A Preparation

**Common Questions:**

**Q: "What if an API fails?"**  
A: "We have fallback mechanisms. For example, the Web agent uses Gemini's knowledge if Google Search quota is exhausted. PatentsView failures fall back to ScrapingDog."

**Q: "Can it handle concurrent users?"**  
A: "Yes, we're using Flask with Gunicorn in production. Each query runs independently. For enterprise scale, we'd recommend containerizing and deploying to Kubernetes."

**Q: "How accurate is the patent analysis?"**  
A: "We query two APIs - PatentsView for breadth and ScrapingDog for depth. The system identifies granted patents, filed applications, and assesses freedom-to-operate risks, but final legal review is recommended."

**Q: "What about data security?"**  
A: "Currently configured for demo purposes. For production, we'd add authentication, encrypt API keys using environment variables, implement CORS restrictions, and add audit logging."

**Q: "Can this be customized for other industries?"**  
A: "Absolutely. The agent framework is modular. You'd replace the Clinical/Patent tools with domain-specific APIs - could be financial data, legal research, or technical literature searches."

---

## Demo Timing
- **Total Demo**: ~3 minutes
- **With Q&A**: ~5-7 minutes
- **Technical Deep-Dive**: ~10-15 minutes

---

## Pro Tips for Live Demo

1. **Pre-load the page** before starting
2. **Have a backup query** ready in case first one fails
3. **Keep PDF viewer open** in background for quick display
4. **Test internet connection** - API calls require stable network
5. **Clear browser cache** before demo for clean tooltip animation
6. **Have STATUS.md open** for technical questions reference
