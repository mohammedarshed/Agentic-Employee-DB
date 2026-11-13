import os

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.tools_schema import employee_tools
from app.agent.tool_executor import execute_tool

load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url=os.getenv("BLUESMINDS_BASE_URL")
)

SYSTEM_PROMPT = (
    "You are an employee management assistant. "
    "Use available tools when database information "
    "is required. Salary values are in INR."
)


def main():
    req = input("Enter your request: ")

    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req}
        ],
        tools=employee_tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # tool_calls is a list (or None if the LLM answered in plain text)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result = execute_tool(tool_call)
            print("Result:", result)
    else:
        print("LLM response:", message.content)


if __name__ == "__main__":
    main()
