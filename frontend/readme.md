# Multi-Agent Automation Engine

Production-ready Streamlit dashboard for enterprise workflow automation using AI-powered multi-agent orchestration with Semantic Kernel.

## Features

- **Multi-Agent Pipeline** - Extraction > Validation > Communication > Reporting
- **Enterprise Scenarios** - 5 pre-built sample workflows (onboarding, expenses, compliance, leave, contracts)
- **File Upload** - Process `.txt` files with enterprise workflow text
- **Real-time Progress** - Visual pipeline progress indicators
- **History Tracking** - Save and review past workflows (requires Cosmos DB)
- **Premium UI** - Clean, responsive design with gradient styling
- **Setup Wizard** - Guided configuration if environment variables are missing

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Azure OpenAI / Microsoft Foundry with a deployed model
- (Optional) Azure Cosmos DB for workflow history persistence

### Step 1: Configure Environment

Copy the example environment file and edit with your credentials:

```bash
copy .env.example .env
```

Edit `.env` with your Azure OpenAI endpoint, API key, and deployment name.

### Step 2: Install Dependencies

```bash
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Architecture

```
User Input (Text / File / Sample)
        ↓
┌─────────────────────────┐
│  Streamlit Dashboard    │
│  (app.py)               │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Orchestrator           │
│  (orchestrator.py)      │
│                         │
│  ┌─ Extraction Agent    │
│  ├─ Validation Agent    │
│  ├─ Communication Agent │
│  └─ Reporting Agent     │
│                         │
│  Powered by:            │
│  Semantic Kernel +      │
│  Azure OpenAI           │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Azure Cosmos DB        │
│  (cosmos_helper.py)     │
│  Shared Memory &        │
│  Audit Trail            │
└─────────────────────────┘
```

## File Structure

```
codefiles/
├── app.py             # Streamlit dashboard (main entry point)
├── orchestrator.py    # Multi-agent orchestrator with all agent definitions
├── cosmos_helper.py   # Cosmos DB persistence helper
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container build file
├── .env.example       # Environment variable template
├── .gitignore         # Git ignore rules
├── README.md          # This file
└── sample_data/       # Sample enterprise scenarios
    ├── employee_onboarding.txt
    ├── expense_report.txt
    ├── compliance_report.txt
    ├── leave_request.txt
    └── vendor_contract.txt
```

## Sample Scenarios

| Scenario | Description |
|----------|-------------|
| **Employee Onboarding** | New hire joining Engineering - extracts name, role, department, equipment needs |
| **Expense Report** | Q4 client visit expenses - extracts items, amounts, approvals |
| **Compliance Report** | Data privacy audit findings - extracts risk levels, action items |
| **Leave Request** | Employee annual leave - extracts dates, coverage plans, approvals |
| **Vendor Contract** | Cloud infrastructure service agreement - extracts terms, amounts, SLAs |

## Docker Deployment

```bash
docker build -t agent-orchestrator .
docker run -p 8501:8501 --env-file .env agent-orchestrator
```
