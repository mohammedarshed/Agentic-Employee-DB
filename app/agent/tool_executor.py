import json

from app.tools.employee_tools import (
    get_employees_by_salary
)


# Map tool names to actual Python functions
TOOL_REGISTRY = {
    "get_employees_by_salary": get_employees_by_salary
}


def execute_tool(tool_call):

    tool_name = tool_call.function.name

    # Find the corresponding Python function
    function = TOOL_REGISTRY.get(tool_name)

    if function is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    # Extract arguments from LLM response
    arguments = json.loads(
        tool_call.function.arguments
    )

    print(f"\nExecuting tool: {tool_name}")
    print(f"Arguments: {arguments}")

    # Execute actual Python function
    print(f"******* Calling the MF tool requested by the LLM *******")
    result = function(**arguments)

    return result
