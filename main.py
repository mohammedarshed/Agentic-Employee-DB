import uuid

from app.database.connection import test_connection
from app.agent.memory import clear_conversation

from app.tools.employee_tools import (
    get_all_employees,
    get_employee_by_id,
    update_employee_salary,
    get_average_salary_by_department
)


from app.tools.employee_tools import get_employees_by_salary

from app.agent.agent import run_agent

if __name__ == "__main__":

    # Create one session for this terminal conversation
    session_id = str(uuid.uuid4())

    print("================================")
    print("  Employee Management AI Agent")
    print("================================")

    print("Session ID:", session_id)
    
    while True:

        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Agent stopped.")
            break

        if user_input.lower() == "/reset":
            clear_conversation(session_id)
            print("Conversation history cleared.")
            continue

        if not user_input:
            continue

        response = run_agent(user_input, session_id)

        print("\nAgent:", response)

# if __name__ == "__main__":


    # # 1. Test connection
    # test_connection()

    # # 2. Get all employees
    # print("\n--- ALL EMPLOYEES ---")
    # employees = get_all_employees()
    # for employee in employees:
    #     print(employee)

    # # 3. Get employee by ID
    # print("\n--- EMPLOYEE BY ID ---")
    # employee = get_employee_by_id(1)
    # print(employee)

    # # 4. Average salary by department
    # print("\n--- DEPARTMENT SALARY ANALYSIS ---")
    # analysis = get_average_salary_by_department()
    # for department in analysis:
    #     print(department)

    # # 5. Update salary (uncomment when ready to test)
    # print("\n--- UPDATE SALARY ---")
    # affected = update_employee_salary(1, 2200000)
    # print("Rows updated:", affected)

    # employees = get_employees_by_salary(1200000)
    # print(employees)

