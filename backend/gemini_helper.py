def get_ai_summary(employee_result: dict) -> str:
    # ✅ Fallback (no API required)
    return f"""
🔍 Analysis for {employee_result['employee_name']}

💸 Total Loss: ₹{employee_result['total_loss']}

⚠️ Issues:
{employee_result['issues']}

⚙️ Actions:
{len(employee_result['actions'])} actions recommended

💡 Suggestion:
Focus on reducing idle time, reassign delayed tasks, and remove unused tools.
"""