import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.tools_schema import employee_tools
from app.agent.tool_executor import execute_tool


load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url=os.getenv("BLUESMINDS_BASE_URL")
)


SYSTEM_PROMPT = """
You are an Employee Management AI Assistant.

You can retrieve employee information using available tools.

Rules:
1. Use tools whenever database information is required.
2. Never invent employee information.
3. Salary values are in Indian Rupees (INR).
4. Explain database results clearly.
5. If a tool returns no records, tell the user.
"""


def run_agent(user_input):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    # Agent execution loop
    for iteration in range(5):

        print("\nCalling LLM...")

        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL"),
            messages=messages,
            tools=employee_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # Add LLM response to conversation
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # If no tool call, return final answer
        if not message.tool_calls:
            return message.content

        # Execute requested tools
        for tool_call in message.tool_calls:

            try:
                result = execute_tool(tool_call)

                tool_result = {
                    "success": True,
                    "data": result
                }

            except Exception as error:

                tool_result = {
                    "success": False,
                    "error": str(error)
                }

            # Send tool result back to LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    default=str
                )
            })

    return "Agent stopped: maximum iterations reached."
