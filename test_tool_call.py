import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.tools_schema import employee_tools

load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url=os.getenv("BLUESMINDS_BASE_URL")
)

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL"),

    messages=[
        {
            "role": "system",
            "content": (
                "You are an employee management assistant. "
                "Use available tools when database information "
                "is required. Salary values are in INR."
            )
        },
        {
            "role": "user",
            "content": "Find employees earning above 12 LPA."
        }
    ],

    tools=employee_tools,
    tool_choice="auto"
)

message = response.choices[0].message

if message.tool_calls:

    for tool_call in message.tool_calls:

        print("Tool selected:", tool_call.function.name)

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("Arguments:", arguments)

else:
    print("LLM response:", message.content)
