from sqlalchemy import text
from app.database.connection import engine

#return type is a dictionary
def get_all_employees():

    query = text("""
        SELECT
            employee_id,
            first_name,
            last_name,
            email,
            annual_salary,
            department_id,
            status
        FROM employees
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        employees = [
            dict(row)
            for row in result.mappings().all()
        ]

        return employees


def get_employee_by_id(employee_id):

    query = text("""
        SELECT *
        FROM employees
        WHERE employee_id = :employee_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"employee_id": employee_id}
        )

        employee = result.mappings().first()

        return dict(employee) if employee else None


def update_employee_salary(employee_id, new_salary):

    if new_salary <= 0:
        raise ValueError("Salary must be greater than zero")

    query = text("""
        UPDATE employees
        SET annual_salary = :new_salary
        WHERE employee_id = :employee_id
    """)

    # Use a transaction to ensure atomicity
    with engine.begin() as connection:

        result = connection.execute(
            query,
            {
                "employee_id": employee_id,
                "new_salary": new_salary
            }
        )

        return result.rowcount


def get_average_salary_by_department():

    query = text("""
        SELECT
            d.department_name,
            ROUND(AVG(e.annual_salary), 2) AS average_salary,
            COUNT(e.employee_id) AS employee_count
        FROM employees e
        JOIN departments d
            ON e.department_id = d.department_id
        GROUP BY d.department_name
    """)

    with engine.connect() as connection:

        result = connection.execute(query)

        return [
            dict(row)
            for row in result.mappings().all()
        ]


def get_employees_by_salary(min_salary):

    query = text("""
        SELECT
            employee_id,
            first_name,
            last_name,
            annual_salary
        FROM employees
        WHERE annual_salary > :min_salary
          AND status = 'ACTIVE'
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {"min_salary": min_salary}
        )

        return [
            dict(row)
            for row in result.mappings().all()
        ]


def add_employee(
    first_name,
    last_name,
    email,
    annual_salary,
    hire_date,
    department_id
):

    if annual_salary <= 0:
        raise ValueError("Salary must be positive")

    query = text("""
        INSERT INTO employees (
            first_name,
            last_name,
            email,
            annual_salary,
            hire_date,
            department_id,
            status
        )
        VALUES (
            :first_name,
            :last_name,
            :email,
            :annual_salary,
            :hire_date,
            :department_id,
            'ACTIVE'
        )
    """)

    with engine.begin() as connection:

        result = connection.execute(
            query,
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "annual_salary": annual_salary,
                "hire_date": hire_date,
                "department_id": department_id
            }
        )

        return result.lastrowid
