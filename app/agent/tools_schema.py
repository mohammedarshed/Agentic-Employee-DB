employee_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employees_by_salary",
            "description": (
                "Find active employees whose annual salary "
                "is greater than the specified amount in INR."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "min_salary": {
                        "type": "number",
                        "description": (
                            "Minimum annual salary in INR"
                        )
                    }
                },
                "required": ["min_salary"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
