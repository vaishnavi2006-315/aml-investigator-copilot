import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AML Investigator Copilot", layout="wide")

st.title("AML Investigator Copilot")
st.caption("AI assistant for suspicious account investigation")

summary = requests.get(f"{API_URL}/summary").json()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", summary["total_transactions"])
c2.metric("Accounts", summary["total_accounts"])
c3.metric("High Risk", summary["high_risk_accounts"])
c4.metric("Suspicious", summary["suspicious_accounts"])

st.divider()

st.subheader("Ask the Copilot")

account_id = st.text_input("Enter Account ID")

if st.button("Investigate"):
    data = requests.get(f"{API_URL}/risk/{account_id}").json()

    if "error" in data:
        st.error("Account not found")
    else:
        st.success("Investigation completed")

        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Score", data["Risk_Score"])
        col2.metric("Risk Level", data["Risk_Level"])
        col3.metric("Suspicious", data["Suspicious_Flag"])

        st.subheader("Copilot Explanation")

        reasons = str(data["Risk_Reasons"])

        if reasons == "nan" or reasons.strip() == "":
            st.write("No strong suspicious reason detected.")
        else:
            for r in reasons.split(";"):
                st.write("•", r.strip())

        st.subheader("Detected Patterns")
        st.write("Smurfing:", data["Smurfing_Flag"])
        st.write("Mule Account:", data["Mule_Flag"])
        st.write("Known Laundering Account:", data["Known_Laundering_Account"])

        st.subheader("Generated AML Report")

        report = f"""
AML INVESTIGATION REPORT

Account ID: {data['Account']}

Risk Score: {data['Risk_Score']}/100
Risk Level: {data['Risk_Level']}

Summary:
This account was analyzed using transaction behavior, laundering labels, and suspicious activity indicators.

Reasons:
{data['Risk_Reasons']}

Red Flags:
- Smurfing Pattern: {data['Smurfing_Flag']}
- Mule Account Behavior: {data['Mule_Flag']}
- Known Laundering Account: {data['Known_Laundering_Account']}
- Suspicious Flag: {data['Suspicious_Flag']}

Recommendation:
{"Escalate for manual AML review." if data["Suspicious_Flag"] else "Continue monitoring."}
"""

        st.text_area("Report", report, height=350)

st.divider()

st.subheader("High Risk Accounts")

high_risk = requests.get(f"{API_URL}/high-risk").json()
st.dataframe(pd.DataFrame(high_risk), use_container_width=True)