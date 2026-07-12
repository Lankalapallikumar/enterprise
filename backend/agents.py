# 🔍 Detection Agent
def detect_issues(emp, tasks, tools):
    issues = []

    if emp["idle_hours"] > 2:
        issues.append("High idle time")

    if any(t["delay_hours"] > 0 for t in tasks):
        issues.append("Task delays present")

    if any(t["used"].lower() == "no" for t in tools):
        issues.append("Unused tools detected")

    return issues

# 💰 Cost Agent
def calculate_costs(emp, tasks, tools):
    idle_loss = emp["idle_hours"] * emp["hourly_cost"]

    delay_loss = sum(t["delay_hours"] * t["penalty_rate"] for t in tasks)

    tool_waste = sum(
        t["license_cost"] for t in tools if t["used"].lower() == "no"
    )

    return idle_loss, delay_loss, tool_waste

# ⚙️ Action Agent
def generate_actions(idle_loss, delay_loss, tool_waste):
    actions = []

    if idle_loss > 0:
        actions.append("Improve workforce utilization")

    if delay_loss > 0:
        actions.append("Reassign delayed tasks")

    if tool_waste > 0:
        actions.append("Deactivate unused licenses")
    return actions
