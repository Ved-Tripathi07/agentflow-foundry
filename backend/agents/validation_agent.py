from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

async def run_validation(kernel: Kernel, extracted_text: str):
    prompt = """
You are a validation agent.

Validate the extracted data below.
Check for missing or inconsistent fields.
Return ONLY valid JSON.

Extracted Data:
{{$data}}
"""

    arguments = KernelArguments(
        data=extracted_text
    )

    result = await kernel.invoke_prompt(
        prompt=prompt,
        arguments=arguments
    )

    return result