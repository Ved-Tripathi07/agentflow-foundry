"""
Multi-Agent Automation Engine - Production Streamlit Application
Enterprise workflow automation using Semantic Kernel multi-agent orchestration
"""

import streamlit as st
import json
import os
import uuid
import asyncio
import time
from datetime import datetime
from dotenv import load_dotenv
import nest_asyncio

nest_asyncio.apply()

from orchestrator import MultiAgentOrchestrator
from cosmos_helper import CosmosHelper

# Load environment variables
load_dotenv()

# ─── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Automation Engine",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Styling ─────────────────────────────────────────────────────
st.markdown(
    """
<style>
    :root {
        --primary: #0078D4;
        --secondary: #50E6FF;
        --success: #107C10;
        --warning: #F7630C;
        --error: #D13438;
    }
    .main-header {
        background: linear-gradient(135deg, #0078D4 0%, #00BCF2 50%, #50E6FF 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,120,212,0.25);
    }
    .main-header h1 { color: white; margin: 0; font-size: 2.3rem; font-weight: 700; }
    .main-header p { color: rgba(255,255,255,0.9); margin: .4rem 0 0 0; font-size: 1.05rem; }
    .status-card {
        background: white; padding: 1rem 1.25rem; border-radius: 8px;
        border-left: 4px solid #0078D4; margin: .5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,.08);
    }
    .status-card.success { border-left-color: #107C10; background: #f0fff0; }
    .status-card.warning { border-left-color: #F7630C; background: #fff8f0; }
    .status-card.error   { border-left-color: #D13438; background: #fff0f0; }
    .agent-card {
        background: #f8f9fa; border-radius: 8px; padding: 1rem;
        border: 1px solid #e0e0e0; margin: .5rem 0;
    }
    .agent-card.active { border-color: #0078D4; background: #f0f7ff; }
    .agent-card.done   { border-color: #107C10; background: #f0fff0; }
    .metric-big { font-size: 2.4rem; font-weight: 700; color: #0078D4; }
    .stButton>button {
        font-weight: 600; border-radius: 6px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 3px 8px rgba(0,0,0,.15); }
    [data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #0078D4; }
    .stTabs [data-baseweb="tab"] { font-weight: 600; padding: .8rem 1.5rem; }
    .stTabs [aria-selected="true"] { border-bottom: 3px solid #0078D4; }
    .completion-banner {
        background: linear-gradient(135deg, #107C10 0%, #00BCF2 100%);
        padding: 1.5rem; border-radius: 10px; margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(16,124,16,0.25);
    }
    .completion-banner h3 { color: white; margin: 0; }
    .completion-banner p { color: rgba(255,255,255,0.9); margin: .3rem 0 0 0; }
</style>
""",
    unsafe_allow_html=True,
)


# ─── Sample Data ─────────────────────────────────────────────────────
SAMPLE_DATA = {}

def load_sample_data():
    """Load sample data from sample_data/ directory."""
    global SAMPLE_DATA
    sample_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    if os.path.exists(sample_dir):
        for filename in sorted(os.listdir(sample_dir)):
            if filename.endswith(".txt"):
                filepath = os.path.join(sample_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                name = filename.replace(".txt", "").replace("_", " ").title()
                SAMPLE_DATA[filename.replace(".txt", "")] = {
                    "name": name,
                    "text": content,
                }

load_sample_data()

# ─── Fallback sample data if files not found ─────────────────────────
if not SAMPLE_DATA:
    SAMPLE_DATA = {
        "employee_onboarding": {
            "name": "Employee Onboarding",
            "text": (
                "New Employee Notification: Jane Doe is joining the Engineering department "
                "as a Senior Software Engineer on March 1, 2026. She will report to Michael "
                "Chen, VP of Engineering. Her employee ID is EMP-2026-0847. She needs a "
                "laptop (MacBook Pro 16-inch), access to GitHub Enterprise, Azure DevOps, "
                "and Slack. Her starting salary is $145,000 with standard benefits. Office "
                "location: Seattle HQ, Floor 12, Desk 12-47. Please complete onboarding "
                "checklist within 5 business days."
            ),
        },
        "expense_report": {
            "name": "Expense Report",
            "text": (
                "Expense Report - Q4 Client Visit: Submitted by Alex Rivera, Sales Director. "
                "Trip to New York, Dec 10-12, 2025. Expenses: Flight SEA-JFK round trip "
                "$487.00, Hotel Marriott Marquis 2 nights $678.00, Client dinner at Nobu "
                "$342.50, Taxi/Uber transportation $156.75, Conference registration fee "
                "$250.00. Total: $1,914.25. Cost center: SALES-2025-Q4. Approved by: "
                "Sarah Kim, SVP Sales. Purpose: Annual contract renewal meeting with "
                "Northwind Traders. Receipt attachments: 5 files."
            ),
        },
        "compliance_report": {
            "name": "Compliance Report",
            "text": (
                "Internal Audit Report - Data Privacy Compliance Review, January 2026. "
                "Auditor: Compliance Team Lead, David Park. Scope: Customer data handling "
                "practices across CRM and Data Analytics teams. Findings: (1) HIGH RISK - "
                "3 databases found with unencrypted PII fields in staging environment. "
                "(2) MEDIUM RISK - Access logs not retained beyond 60 days, policy requires "
                "180 days. (3) LOW RISK - 12 employee accounts still active after departure. "
                "Recommendation: Encrypt all PII at rest within 30 days. Extend log retention "
                "to 180 days. Implement automated offboarding workflow. Next review: April 2026."
            ),
        },
        "leave_request": {
            "name": "Leave Request",
            "text": (
                "Leave Request: Employee Sarah Johnson (EMP-2024-0312), Marketing Manager, "
                "requests annual leave from March 15 to March 22, 2026 (6 working days). "
                "Reason: Family vacation. Remaining balance: 14 days. Coverage plan: "
                "James Wilson (Marketing Lead) will handle urgent items. All campaign "
                "deadlines met before departure. Manager approval required from: Lisa "
                "Chen, VP Marketing. Emergency contact during leave: (206) 555-0189."
            ),
        },
        "vendor_contract": {
            "name": "Vendor Contract",
            "text": (
                "Vendor Agreement Summary: Contoso Enterprises is entering a 24-month "
                "service contract with CloudTech Solutions for managed cloud infrastructure. "
                "Contract ID: VND-2026-0093. Start date: April 1, 2026. Monthly fee: "
                "$12,500. Total contract value: $300,000. Services include: 24/7 monitoring, "
                "incident response (SLA 15 min critical, 1 hour high), monthly performance "
                "reports, quarterly business reviews. Auto-renewal unless 90-day notice given. "
                "Primary contact: Tom Bradley, CloudTech Account Manager. Signed by: CFO "
                "Jennifer Walsh, Contoso Enterprises. Legal review completed Feb 10, 2026."
            ),
        },
    }


# ─── Configuration Validation ────────────────────────────────────────
def validate_config():
    """Check required environment variables."""
    required = {
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "MICROSOFT_FOUNDRY_API_KEY": os.getenv("MICROSOFT_FOUNDRY_API_KEY"),
        "AZURE_DEPLOYMENT_NAME": os.getenv("AZURE_DEPLOYMENT_NAME"),
    }
    optional = {
        "COSMOS_DB_ENDPOINT": os.getenv("COSMOS_DB_ENDPOINT"),
        "COSMOS_DB_KEY": os.getenv("COSMOS_DB_KEY"),
    }
    missing_req = [k for k, v in required.items() if not v or v.strip() == ""]
    missing_opt = [k for k, v in optional.items() if not v or v.strip() == ""]
    return missing_req, missing_opt


def show_setup_guide(missing_req, missing_opt):
    """Display setup guide for missing configuration."""
    st.error("⚙️ **Configuration Required**")
    st.markdown("""
### Quick Setup Guide

Edit the `.env` file in the codefiles folder with your credentials.
""")
    if missing_req:
        st.warning(f"**Missing Required Variables:** {', '.join(missing_req)}")
        st.markdown("""
**Get Azure OpenAI Endpoint & Key:**
1. Go to [Azure Portal](https://portal.azure.com)
2. Open your Microsoft Foundry resource → **Keys and Endpoint**
3. Copy the **Endpoint** and **Key 1**

**Deployment Name:** Use `agent-gpt-4o-mini` (from Challenge 1)
""")
    if missing_opt:
        st.info(f"**Optional (for history):** {', '.join(missing_opt)}")
        st.markdown("""
**Get Cosmos DB credentials:**
1. Azure Portal → Cosmos DB account → **Keys**
2. Copy **URI** and **Primary Key**
""")
    st.markdown("""
After configuring `.env`, restart the application.
""")
    st.stop()


# ─── Validate at startup ─────────────────────────────────────────────
missing_req, missing_opt = validate_config()
if missing_req:
    show_setup_guide(missing_req, missing_opt)


# ─── Initialize Services ─────────────────────────────────────────────
@st.cache_resource
def get_orchestrator():
    """Initialize the multi-agent orchestrator."""
    return MultiAgentOrchestrator(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("MICROSOFT_FOUNDRY_API_KEY"),
        deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
    )


@st.cache_resource
def get_cosmos():
    """Initialize Cosmos DB helper (returns None if not configured)."""
    endpoint = os.getenv("COSMOS_DB_ENDPOINT")
    key = os.getenv("COSMOS_DB_KEY")
    database = os.getenv("COSMOS_DB_DATABASE", "agent-memory-db")
    container = os.getenv("COSMOS_DB_CONTAINER", "agent-state")
    if endpoint and key:
        try:
            return CosmosHelper(endpoint, key, database, container)
        except Exception as e:
            st.sidebar.warning(f"Cosmos DB unavailable: {e}")
            return None
    return None


orchestrator = get_orchestrator()
cosmos = get_cosmos()


# ─── Header ──────────────────────────────────────────────────────────
st.markdown(
    """
<div class="main-header">
    <h1>⚙️ Multi-Agent Automation Engine</h1>
    <p>Enterprise workflow automation powered by AI agent collaboration &amp; Semantic Kernel</p>
</div>
""",
    unsafe_allow_html=True,
)


# ─── Sidebar ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 Agent Pipeline")
    agents = [
        ("Extraction Agent", "Extracts structured data"),
        ("Validation Agent", "Validates data quality"),
        ("Communication Agent", "Generates notifications"),
        ("Reporting Agent", "Produces summaries"),
    ]
    for name, desc in agents:
        st.markdown(f"✅ **{name}**  \n{desc}")

    st.divider()
    st.markdown("## 📊 Configuration")
    st.markdown(f"**Model:** `{os.getenv('AZURE_DEPLOYMENT_NAME', 'N/A')}`")
    st.markdown(f"**Cosmos DB:** {'🟢 Connected' if cosmos else '🔴 Not configured'}")

    st.divider()
    st.markdown("## 📁 Sample Scenarios")
    st.markdown(f"**{len(SAMPLE_DATA)}** enterprise scenarios available")
    for key, data in SAMPLE_DATA.items():
        st.markdown(f"- {data['name']}")


# ─── Main Tabs ───────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔄 Process Workflow", "📋 Results", "📜 History"])


# ─── Tab 1: Process Workflow ─────────────────────────────────────────
with tab1:
    col_input, col_sample = st.columns([3, 1])

    with col_sample:
        st.markdown("### 📁 Sample Data")
        sample_choice = st.selectbox(
            "Select a scenario:",
            ["-- Select --"] + [d["name"] for d in SAMPLE_DATA.values()],
            key="sample_select",
        )
        if st.button("📥 Load Sample", use_container_width=True):
            if sample_choice != "-- Select --":
                for key, data in SAMPLE_DATA.items():
                    if data["name"] == sample_choice:
                        st.session_state["input_text"] = data["text"]
                        st.rerun()

        st.markdown("---")
        st.markdown("### 📤 Upload File")
        uploaded = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded:
            content = uploaded.read().decode("utf-8")
            st.session_state["input_text"] = content
            st.rerun()

    with col_input:
        st.markdown("### 📝 Workflow Input")
        st.markdown("Enter enterprise workflow text, select a sample scenario, or upload a file.")

        input_text = st.text_area(
            "Workflow text:",
            value=st.session_state.get("input_text", ""),
            height=250,
            placeholder="Paste or type your enterprise workflow text here...\n\nExample: New employee joining, expense report, compliance finding, leave request, vendor contract...",
            key="workflow_input",
        )

        if st.button("🚀 Run Pipeline", type="primary", use_container_width=True):
            if not input_text or input_text.strip() == "":
                st.error("Please enter workflow text, select a sample, or upload a file.")
            else:
                workflow_id = str(uuid.uuid4())
                st.session_state["current_workflow_id"] = workflow_id
                st.session_state["current_input"] = input_text

                progress_container = st.container()
                with progress_container:
                    st.markdown("---")
                    st.markdown("### ⏳ Pipeline Execution")

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    agent_steps = [
                        ("Extraction Agent", "Extracting structured data..."),
                        ("Validation Agent", "Validating data quality..."),
                        ("Communication Agent", "Generating communication..."),
                        ("Reporting Agent", "Producing summary report..."),
                    ]

                    results = {}
                    workflow_state = {
                        "id": workflow_id,
                        "workflowId": workflow_id,
                        "currentStep": "starting",
                        "status": "IN_PROGRESS",
                        "agentData": {},
                        "history": [],
                        "input": input_text[:500],
                        "timestamp": datetime.utcnow().isoformat(),
                    }

                    all_success = True

                    for i, (agent_name, agent_desc) in enumerate(agent_steps):
                        status_text.markdown(
                            f'<div class="agent-card active">🔄 <strong>{agent_name}</strong> - {agent_desc}</div>',
                            unsafe_allow_html=True,
                        )
                        progress_bar.progress((i) / len(agent_steps))

                        try:
                            step_key = agent_name.split()[0].lower()
                            result = asyncio.run(
                                orchestrator.run_single_agent(step_key, input_text if i == 0 else results.get(prev_key, ""), workflow_state)
                            )
                            results[step_key] = result
                            workflow_state["agentData"][step_key] = str(result)
                            workflow_state["history"].append({
                                "agent": agent_name,
                                "output": str(result),
                                "timestamp": datetime.utcnow().isoformat(),
                            })
                            workflow_state["currentStep"] = step_key
                            prev_key = step_key

                            status_text.markdown(
                                f'<div class="agent-card done">✅ <strong>{agent_name}</strong> - Complete</div>',
                                unsafe_allow_html=True,
                            )
                            time.sleep(0.3)

                        except Exception as e:
                            all_success = False
                            st.error(f"❌ {agent_name} failed: {str(e)}")
                            workflow_state["status"] = "FAILED"
                            workflow_state["error"] = str(e)
                            break

                    if all_success:
                        progress_bar.progress(1.0)
                        workflow_state["currentStep"] = "completed"
                        workflow_state["status"] = "COMPLETED"

                        # Save to Cosmos DB
                        if cosmos:
                            try:
                                cosmos.save_workflow_state(workflow_state)
                            except Exception as e:
                                st.warning(f"Could not save to Cosmos DB: {e}")

                        st.session_state["last_results"] = results
                        st.session_state["last_workflow_state"] = workflow_state

                        st.markdown(
                            """
<div class="completion-banner">
    <h3>✅ Pipeline Completed Successfully!</h3>
    <p>All four agents executed. Switch to the <strong>Results</strong> tab to view outputs.</p>
</div>
""",
                            unsafe_allow_html=True,
                        )

                        status_text.markdown(
                            f'<div class="status-card success">🎯 <strong>Workflow ID:</strong> <code>{workflow_id}</code> | Status: <strong>COMPLETED</strong></div>',
                            unsafe_allow_html=True,
                        )


# ─── Tab 2: Results ──────────────────────────────────────────────────
with tab2:
    if "last_results" not in st.session_state:
        st.info("No results yet. Run a workflow from the **Process Workflow** tab.")
    else:
        results = st.session_state["last_results"]
        ws = st.session_state["last_workflow_state"]

        st.markdown(
            f"""
<div class="status-card success">
    <strong>Workflow ID:</strong> <code>{ws.get('id', 'N/A')}</code> &nbsp;|&nbsp;
    <strong>Status:</strong> {ws.get('status', 'N/A')} &nbsp;|&nbsp;
    <strong>Timestamp:</strong> {ws.get('timestamp', 'N/A')}
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Four columns for agent results
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔍 Extraction Agent")
            extraction = results.get("extraction", "No output")
            st.code(str(extraction), language="json")

        with col2:
            st.markdown("### ✅ Validation Agent")
            validation = results.get("validation", "No output")
            st.code(str(validation), language="json")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("### 📧 Communication Agent")
            communication = results.get("communication", "No output")
            st.code(str(communication), language="json")

        with col4:
            st.markdown("### 📊 Reporting Agent")
            reporting = results.get("reporting", "No output")
            st.code(str(reporting), language="json")

        st.markdown("---")
        with st.expander("📄 Full Workflow State (JSON)"):
            st.json(ws)


# ─── Tab 3: History ──────────────────────────────────────────────────
with tab3:
    if not cosmos:
        st.info(
            "📜 History requires Cosmos DB configuration. Add `COSMOS_DB_ENDPOINT` and `COSMOS_DB_KEY` to your `.env` file."
        )
    else:
        st.markdown("### 📜 Workflow Execution History")
        if st.button("🔄 Refresh History"):
            st.rerun()

        try:
            history = cosmos.get_all_workflows()
            if not history:
                st.info("No workflow history found. Run a workflow to see entries here.")
            else:
                st.metric("Total Workflows", len(history))
                st.markdown("---")

                for wf in sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True):
                    wf_id = wf.get("id", "N/A")
                    status = wf.get("status", "UNKNOWN")
                    ts = wf.get("timestamp", "N/A")
                    step = wf.get("currentStep", "N/A")
                    input_preview = wf.get("input", "")[:100]

                    status_icon = "✅" if status == "COMPLETED" else "❌" if status == "FAILED" else "⏳"

                    with st.expander(f"{status_icon} {wf_id[:8]}... | {status} | {ts}"):
                        st.markdown(f"**Input Preview:** {input_preview}...")
                        st.markdown(f"**Current Step:** {step}")
                        st.markdown(f"**Status:** {status}")

                        agent_data = wf.get("agentData", {})
                        if agent_data:
                            st.markdown("**Agent Outputs:**")
                            for agent, output in agent_data.items():
                                st.markdown(f"**{agent.title()}:**")
                                st.code(str(output)[:500], language="json")

                        history_entries = wf.get("history", [])
                        if history_entries:
                            st.markdown(f"**Execution Steps:** {len(history_entries)} agents")

        except Exception as e:
            st.error(f"Error loading history: {e}")
