from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

async def run_extraction(kernel: Kernel, input_text: str):
  prompt = """
You are an extraction agent.

Extract structured data from the text below.
Return ONLY valid JSON.

Text:
{{$inputText}}
"""

  arguments = KernelArguments(
      inputText=input_text
  )

  result = await kernel.invoke_prompt(
      prompt,
      arguments=arguments
  )

  return result