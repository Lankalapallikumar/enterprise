from fastapi import FastAPI
from backend.logic import analyze_enterprise_data
from backend.gemini_helper import get_ai_summary


app = FastAPI()



@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/analyze")
def analyze():
    return analyze_enterprise_data()


@app.get("/summary/{employee_id}")
def summary(employee_id: int):
    data = analyze_enterprise_data()

    emp = next((e for e in data if e["employee_id"] == employee_id), None)

    if not emp:
        return {"error": "Employee not found"}

    return {
        "employee_id": employee_id,
        "ai_summary": get_ai_summary(emp)
    }