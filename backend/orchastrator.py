from agents.extraction_agent import run_extraction
from agents.validation_agent import run_validation
from agents.communication_agent import run_communication
from agents.reporting_agent import run_reporting
from storage.cosmos_client import save_workflow_state

async def run_workflow(kernel, workflow_id, input_text):
    workflow_state = {
        "id": workflow_id,
        "workflowId": workflow_id,
        "currentStep": "extraction",
        "status": "IN_PROGRESS",
        "agentData": {},
        "history": []
    }

    # Step 1: Extraction
    extraction_result = await run_extraction(kernel, input_text)
    extraction_output = str(extraction_result)

    workflow_state["agentData"]["extraction"] = extraction_output
    workflow_state["history"].append({
        "agent": "ExtractionAgent",
        "output": extraction_output
    })
    workflow_state["currentStep"] = "validation"
    save_workflow_state(workflow_state)

    # Step 2: Validation
    validation_result = await run_validation(kernel, extraction_output)
    validation_output = str(validation_result)

    workflow_state["agentData"]["validation"] = validation_output
    workflow_state["history"].append({
        "agent": "ValidationAgent",
        "output": validation_output
    })
    workflow_state["currentStep"] = "communication"
    save_workflow_state(workflow_state)

    # Step 3: Communication
    communication_result = await run_communication(kernel, validation_output)
    communication_output = str(communication_result)

    workflow_state["agentData"]["communication"] = communication_output
    workflow_state["history"].append({
        "agent": "CommunicationAgent",
        "output": communication_output
    })
    workflow_state["currentStep"] = "reporting"
    save_workflow_state(workflow_state)

    # Step 4: Reporting
    reporting_result = await run_reporting(kernel, workflow_state)
    reporting_output = str(reporting_result)

    workflow_state["agentData"]["reporting"] = reporting_output
    workflow_state["history"].append({
        "agent": "ReportingAgent",
        "output": reporting_output
    })

    workflow_state["currentStep"] = "completed"
    workflow_state["status"] = "COMPLETED"
    save_workflow_state(workflow_state)

    return workflow_state