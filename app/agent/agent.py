import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from app.agent.tools_schema import employee_tools
from app.agent.tool_executor import execute_tool

from app.agent.memory import get_conversation

load_dotenv()

client = OpenAI(
    api_key=os.getenv("BLUESMINDS_API_KEY"),
    base_url=os.getenv("BLUESMINDS_BASE_URL")
)

SYSTEM_PROMPT = """
You are an Employee Management AI Assistant.

You have access to tools that interact with a MySQL database.

Your capabilities:

1. Retrieve all employees.
2. Find employees by ID.
3. Find employees by salary.
4. Analyse department salaries.
5. Update employee salaries.
6. Add new employees.

Rules:

1. Use tools whenever database information is required.
2. Never invent employee information.
3. Salary values are in INR.
4. Convert LPA into annual INR.
   Example: 12 LPA = 1200000.
5. Never claim an operation succeeded unless
   the tool confirms success.
6. Never attempt write operations unless
   explicitly requested by the user.
7. If a write operation is cancelled,
   clearly inform the user.
8. Present database results clearly.
9. Use web_search only for external or current information that is not
   in the employee database. Cite the source URLs you used.
"""


def run_agent(user_input, session_id):

    messages = get_conversation(session_id, SYSTEM_PROMPT)

    #Add the new user Message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # Agent execution loop
    for i, n in enumerate(range(5)):

        print(f"\nCalling LLM... {{iteration: {i+1}}}")

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

        # Check whether LLM requested a tool
        if not message.tool_calls:
            return message.content

        # Execute requested tools
        for tool_call in message.tool_calls:

            try:
                result = execute_tool(tool_call)

                # Preserve success/cancelled status
                tool_result = {
                    "success": True,
                    "data": result
                }

                print(f"\n --- Tool result: {tool_result} --- ")

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
