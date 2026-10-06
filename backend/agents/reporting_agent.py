from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

async def run_reporting(kernel: Kernel, workflow_data):
    prompt = """
You are a reporting agent.

Summarize the workflow execution below.
Return ONLY valid JSON.

Workflow State:
{{$data}}
"""

    arguments = KernelArguments(
        data=str(workflow_data)
    )

    result = await kernel.invoke_prompt(
        prompt=prompt,
        arguments=arguments
    )

    return result