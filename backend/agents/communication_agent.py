from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

async def run_communication(kernel: Kernel, validated_text: str):
    prompt = """
You are a communication agent.

Draft a professional email based on the validated data below.
Return ONLY valid JSON with subject and body.

Validated Data:
{{$data}}
"""

    arguments = KernelArguments(
        data=validated_text
    )

    result = await kernel.invoke_prompt(
        prompt=prompt,
        arguments=arguments
    )

    return result