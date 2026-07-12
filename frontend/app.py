import streamlit as st
import requests
import pandas as pd
st.set_page_config(page_title="Enterprise AI", layout="wide", page_icon="💰")

# HEADER
st.markdown("# 💰 Enterprise Cost Intelligence Platform")
st.markdown("### 🚀 Detect • Analyze • Act • Optimize")
st.markdown("---")

API_URL = "http://127.0.0.1:8000"

try:
    data = requests.get(f"{API_URL}/analyze").json()
    df = pd.DataFrame(data)

    # ================= KPI =================
    st.markdown("## 📊 Enterprise Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💸 Total Loss", f"₹{df['total_loss'].sum():,.0f}")
    c2.metric("⚠️ Idle Cost", f"₹{df['idle_loss'].sum():,.0f}")
    c3.metric("⏳ Delay Cost", f"₹{df['delay_loss'].sum():,.0f}")
    c4.metric("🛠 Tool Waste", f"₹{df['tool_waste'].sum():,.0f}")

    st.markdown("---")

    # ================= CHARTS =================
    st.markdown("## 📊 Cost Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cost Breakdown")
        st.caption("Where money is leaking")

        breakdown = pd.DataFrame({
            "Category": ["Idle", "Delay", "Tools"],
            "Cost": [
                df["idle_loss"].sum(),
                df["delay_loss"].sum(),
                df["tool_waste"].sum()
            ]
        })

        st.bar_chart(breakdown.set_index("Category"))

    with col2:
        st.subheader("Loss by Employee")
        st.caption("Top contributors")

        st.bar_chart(df.set_index("employee_name")["total_loss"])

    st.markdown("---")

    # ================= EMPLOYEE =================
    st.markdown("## 🧠 Employee Insights")

    for emp in data:
        with st.expander(f"👤 {emp['employee_name']} | ₹{emp['total_loss']:,.0f}"):

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("### 📌 Metrics")
                st.write(f"Utilization: {emp['utilization_pct']}%")
                st.write(f"Idle Hours: {emp['idle_hours']}")
                st.write(f"SLA Risk: {emp['sla_risk']}")

                st.markdown("### 💸 Cost Breakdown")
                st.write(f"Idle: ₹{emp['idle_loss']}")
                st.write(f"Delay: ₹{emp['delay_loss']}")
                st.write(f"Tools: ₹{emp['tool_waste']}")

            with c2:
                st.markdown("### ⚠️ Issues")
                for i in emp["issues"]:
                    st.warning(i)

                st.markdown("### 🔍 Root Causes")
                for r in emp["root_causes"]:
                    st.info(r)

            st.markdown("### ⚙️ Actions")
            for a in emp["actions"]:
                st.write(
                    f"👉 {a['action']} | Risk: {a['risk_level']} | 💰 ₹{a['estimated_savings']}"
                )

            # AI BUTTON
            if st.button(f"🤖 AI Suggestion {emp['employee_id']}"):
                res = requests.get(f"{API_URL}/summary/{emp['employee_id']}")
                st.success(res.json()["ai_summary"])

    # ================= ACTION ENGINE =================
    st.markdown("---")
    st.markdown("## ⚡ Autonomous Action Engine")

    if st.button("🚀 Execute Smart Actions"):
        executed = df["executed_savings"].sum()
        projected = df["projected_savings_if_all_approved"].sum()

        st.success("Actions executed successfully")

        st.write(f"✔ Executed Savings: ₹{executed:,.0f}")
        st.write(f"📈 Potential Savings: ₹{projected:,.0f}")

        st.balloons()

    # ================= FOOTER =================
    st.markdown("---")
    st.markdown("### 🚀 Enterprise AI Cost Optimization System")

except Exception as e:
    st.error(f"Error: {e}")
