from sqlalchemy.orm import Session
from app.models.employee_info import EmployeeInfo
from app.models.training import Training


def get_employees_data(db: Session):
    employees_data = db.query(
        EmployeeInfo,
        Training
    ).outerjoin(
        Training,
        EmployeeInfo.id == Training.employee_id
    ).order_by(
        EmployeeInfo.name
    ).all()

    employees = []
    for emp_info, edu_info in employees_data:
        employees.append({
            "employee": emp_info,
            "education": edu_info if edu_info else None
        })
    return employees