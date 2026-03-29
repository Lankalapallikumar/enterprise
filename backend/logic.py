import pandas as pd
from backend.data_loader import load_all_data
from backend.agents import detect_issues, calculate_costs, generate_actions


def get_existing_approval_status(approvals: pd.DataFrame, employee_id: int, action_name: str):
    rows = approvals[
        (approvals["employee_id"] == employee_id)
        & (approvals["action_type"].str.strip().str.lower() == action_name.strip().lower())
    ]
    if len(rows) > 0:
        row = rows.iloc[0]
        return {
            "status": row["status"],
            "approver": row["approver"],
            "risk_level": row["risk_level"],
        }
    return None


def analyze_enterprise_data():
    workforce, tasks, tools, approvals = load_all_data()
    results = []

    for _, emp in workforce.iterrows():
        employee_id = int(emp["employee_id"])

        task_rows = tasks[tasks["employee_id"] == employee_id]
        tool_rows = tools[tools["employee_id"] == employee_id]

        task_list = task_rows.to_dict("records")
        tool_list = tool_rows.to_dict("records")

        issues = detect_issues(emp, task_list, tool_list)

        idle_loss, delay_loss, tool_waste = calculate_costs(emp, task_list, tool_list)

        total_loss = idle_loss + delay_loss + tool_waste

        sla_risk = "Yes" if any(t["sla_breach_risk"] == "Yes" for t in task_list) else "No"

        delayed_tasks = [t["task_name"] for t in task_list if t["delay_hours"] > 0]
        unused_tools = [t["tool_name"] for t in tool_list if t["used"].lower() == "no"]

        root_causes = []
        if idle_loss > 0:
            root_causes.append(f"Idle hours → ₹{idle_loss}")
        if delay_loss > 0:
            root_causes.append(f"Delayed tasks: {', '.join(delayed_tasks)}")
        if tool_waste > 0:
            root_causes.append(f"Unused tools: {', '.join(unused_tools)}")

        actions = []

        if idle_loss > 0:
            actions.append({
                "action": "Focus Intervention",
                "risk_level": "Low",
                "status": "Approved",
                "estimated_savings": round(idle_loss * 0.3, 2),
            })

        if delay_loss > 0:
            actions.append({
                "action": "Task Reassignment",
                "risk_level": "High",
                "status": "Pending",
                "estimated_savings": round(delay_loss * 0.5, 2),
            })

        if tool_waste > 0:
            actions.append({
                "action": "Deactivate Licenses",
                "risk_level": "Medium",
                "status": "Pending",
                "estimated_savings": round(tool_waste, 2),
            })

        executed_savings = sum(a["estimated_savings"] for a in actions if a["status"] == "Approved")
        projected_savings = sum(a["estimated_savings"] for a in actions)

        results.append({
            "employee_id": employee_id,
            "employee_name": emp["employee_name"],
            "team": emp["team"],
            "utilization_pct": emp["utilization_pct"],
            "idle_hours": emp["idle_hours"],
            "idle_loss": idle_loss,
            "delay_loss": delay_loss,
            "tool_waste": tool_waste,
            "total_loss": total_loss,
            "sla_risk": sla_risk,
            "issues": issues,
            "root_causes": root_causes,
            "actions": actions,
            "executed_savings": executed_savings,
            "projected_savings_if_all_approved": projected_savings,
        })

    return results