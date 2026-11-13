
employee_tools = [
    # 0. Web search
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current or external information "
                "that is NOT in the employee database (e.g. market "
                "salary benchmarks, company news, general facts). "
                "Never use it for employee records."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results (1-10)"
                    }
                },
                "required": ["query", "max_results"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 1. Get all employees
    {
        "type": "function",
        "function": {
            "name": "get_all_employees",
            "description": "Retrieve all employee records.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 2. Get employee by ID
    {
        "type": "function",
        "function": {
            "name": "get_employee_by_id",
            "description": "Find an employee using employee ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {"type": "integer"}
                },
                "required": ["employee_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 3. Get employees by salary
    {
        "type": "function",
        "function": {
            "name": "get_employees_by_salary",
            "description": "Find active employees earning above a specified annual salary in INR.",
            "parameters": {
                "type": "object",
                "properties": {
                    "min_salary": {"type": "number"}
                },
                "required": ["min_salary"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 4. Department salary analysis
    {
        "type": "function",
        "function": {
            "name": "get_average_salary_by_department",
            "description": "Calculate average salary and employee count for each department.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 5. Update employee salary
    {
        "type": "function",
        "function": {
            "name": "update_employee_salary",
            "description": "Update the annual salary of an active employee. Use only when explicitly requested by the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {"type": "integer"},
                    "new_salary": {"type": "number"}
                },
                "required": ["employee_id", "new_salary"],
                "additionalProperties": False
            },
            "strict": True
        }
    },

    # 6. Add employee
    {
        "type": "function",
        "function": {
            "name": "add_employee",
            "description": "Create a new active employee record.",
            "parameters": {
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "email": {"type": "string"},
                    "annual_salary": {"type": "number"},
                    "hire_date": {"type": "string"},
                    "department_id": {"type": "integer"}
                },
                "required": [
                    "first_name",
                    "last_name",
                    "email",
                    "annual_salary",
                    "hire_date",
                    "department_id"
                ],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
