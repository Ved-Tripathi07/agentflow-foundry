# AgentFlow Foundry

AgentFlow Foundry is a multi-agent workflow automation project built with Semantic Kernel, Azure OpenAI, Streamlit, and Azure Cosmos DB. It is designed to process business workflow text, pass it through specialized AI agents, and present the results in a dashboard-oriented experience.

This repository currently contains two major parts:

- `backend/` for workflow orchestration, agent execution, and persistence.
- `frontend/` for the Streamlit user interface and operator experience.

## Why this name

`AgentFlow Foundry` fits the project well because it combines the two core ideas in the codebase:

- `AgentFlow`: the system routes work through multiple agents in sequence.
- `Foundry`: the project is built around Azure OpenAI / Microsoft Foundry-style infrastructure and enterprise workflow automation.

If you want a shorter GitHub repo name, `agentflow-foundry` is a strong option.

## What the project does

The system takes enterprise-style workflow input such as onboarding requests, compliance findings, leave requests, or vendor summaries and processes that input through a four-step agent pipeline:

1. Extraction
2. Validation
3. Communication
4. Reporting

The goal is to turn unstructured operational text into structured outputs, generated communication, and workflow history that can be reviewed later.

## Core capabilities

- Multi-agent workflow pipeline using Semantic Kernel
- Azure OpenAI integration for prompt-driven task execution
- Streamlit dashboard for interactive input and workflow review
- Cosmos DB persistence for workflow history and state tracking
- Sample enterprise scenarios for testing and demos
- Modular agent layout for future expansion

## Architecture

```text
User Input / Sample Data / Uploaded Text
                |
                v
        Streamlit Frontend
          frontend/app.py
                |
                v
      Workflow Orchestration Layer
      backend/main.py
      backend/orchastrator.py
                |
                v
        Specialized AI Agents
      - extraction_agent
      - validation_agent
      - communication_agent
      - reporting_agent
                |
                v
          Cosmos DB Storage
      backend/storage/cosmos_client.py
```

## Repository structure

```text
multi-agent-engine/
├── README.md
├── requirements.txt
├── backend/
│   ├── main.py
│   ├── orchastrator.py
│   ├── agents/
│   │   ├── communication_agent.py
│   │   ├── extraction_agent.py
│   │   ├── reporting_agent.py
│   │   └── validation_agent.py
│   └── storage/
│       └── cosmos_client.py
└── frontend/
    ├── app.py
    ├── cosmos_helper.py
    ├── dockerfile
    ├── readme.md
    ├── requirements.py
    ├── .env.example
    └── .gitignore
```

## Technology stack

- Python
- Streamlit
- Semantic Kernel
- Azure OpenAI / Microsoft Foundry
- Azure Cosmos DB
- python-dotenv
- nest_asyncio

## Setup

### Prerequisites

- Python 3.11+
- An Azure OpenAI or Microsoft Foundry deployment
- Optional Azure Cosmos DB account for workflow history

### Install dependencies

Install the shared backend dependencies from the repository root:

```bash
pip install -r requirements.txt
```

Install the frontend dependencies from the frontend folder definition:

```bash
pip install -r frontend/requirements.py
```

### Environment configuration

Create or update an environment file with values for:

```env
AZURE_OPENAI_ENDPOINT=
MICROSOFT_FOUNDRY_API_KEY=
AZURE_DEPLOYMENT_NAME=
MICROSOFT_FOUNDRY_VERSION=
COSMOS_DB_ENDPOINT=
COSMOS_DB_KEY=
COSMOS_DB_DATABASE=
COSMOS_DB_CONTAINER=
```

The frontend already includes an example template at `frontend/.env.example`.

### Running the project

At a conceptual level:

- `backend/` contains the workflow engine.
- `frontend/` contains the Streamlit UI.

The intended primary UI entry point is:

```bash
streamlit run frontend/app.py
```

The backend runner is located at:

```bash
python backend/main.py
```

## Current repository status

This repository is structurally clear now that it is split into `backend/` and `frontend/`, but there are still integration details to clean up before treating it as fully production-ready.

Current gaps visible from the codebase:

- The frontend imports an `orchestrator` module that is not currently present in `frontend/`.
- The backend orchestration file is named `orchastrator.py`, which may require import alignment.
- The frontend dependency file is named `requirements.py`, even though it is being used as a pip requirements file.

For a GitHub push, this README is accurate, but the codebase would benefit from one integration pass to make the frontend and backend runnable together with a single documented command.

## Roadmap ideas

- Unify frontend and backend imports
- Standardize naming from `orchastrator` to `orchestrator`
- Add a single top-level entry point
- Add tests for each agent stage
- Add API endpoints if a non-Streamlit client is needed later

## Recommended GitHub description

Multi-agent enterprise workflow automation platform built with Semantic Kernel, Azure OpenAI, Streamlit, and Cosmos DB.