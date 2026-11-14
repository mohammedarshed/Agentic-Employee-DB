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

    try:
        tool_name = tool_call.function.name

        # Find the corresponding Python function
        function = TOOL_REGISTRY.get(tool_name)

        if function is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        # Extract arguments from LLM response
        arguments = json.loads(
            tool_call.function.arguments
        )

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
                return create_tool_response(
                    status="cancelled",
                    message="User did not approve the operation."
                )

        # Execute the tool function with the provided arguments
        result = function(**arguments)

        return create_tool_response(
            status="success",
            data=result
        )
    
    except Exception as error:
        print(f"Tool execution error: {error}")

        # 8. Return standardized error response
        return create_tool_response(
            status="error",
            message=str(error)
        )

# 3. Standard response builder
def create_tool_response(status, data=None, message=None):

    return {
        "status": status,
        "data": data,
        "message": message
    }