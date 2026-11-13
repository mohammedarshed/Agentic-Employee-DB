import json

from app.tools.employee_tools import (
    get_all_employees,
    get_employee_by_id,
    get_employees_by_salary,
    get_average_salary_by_department,
    update_employee_salary,
    add_employee
)

from app.tools.web_search import web_search


# Map tool names to actual Python functions
TOOL_REGISTRY = {
    "get_all_employees": get_all_employees,
    "get_employee_by_id": get_employee_by_id,
    "get_employees_by_salary": get_employees_by_salary,
    "get_average_salary_by_department":
        get_average_salary_by_department,
    "update_employee_salary": update_employee_salary,
    "add_employee": add_employee,
    "web_search": web_search
}

# These tools modify database records
WRITE_TOOLS = {
    "update_employee_salary",
    "add_employee"
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
    print(f"\nTool selected: {tool_name}")
    print(f"Arguments: {arguments}")

    # Human confirmation before write operations
    if tool_name in WRITE_TOOLS:

        print("\nWARNING: This operation modifies MySQL!")

        confirmation = input(
            "Do you want to proceed? (Y/N): "
        ).strip().lower()

        if confirmation != "y":
            return {
                "status": "cancelled",
                "message": "User did not approve the operation."
            }

    result = function(**arguments)

    return {
        "status": "success",
        "data": result
    }
