import os
import asyncio
import uuid
from dotenv import load_dotenv

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from orchestrator import run_workflow

load_dotenv()

async def main():
    kernel = Kernel()

    kernel.add_service(
        AzureChatCompletion(
            service_id="chat",
            deployment_name=os.environ["AZURE_DEPLOYMENT_NAME"],
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["MICROSOFT_FOUNDRY_API_KEY"],
            api_version=os.environ["MICROSOFT_FOUNDRY_VERSION"]
        )
    )

    workflow_id = str(uuid.uuid4())
    input_text = "Employee Jane Doe joins Engineering on Feb 1, 2026."

    final_state = await run_workflow(kernel, workflow_id, input_text)

    print("Workflow completed")
    print("Workflow ID:", workflow_id)

if __name__ == "__main__":
    asyncio.run(main())