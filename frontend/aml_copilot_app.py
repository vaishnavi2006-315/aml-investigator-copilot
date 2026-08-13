import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AML Investigator Copilot",
    layout="wide"
)

st.title("AML Investigator Copilot")
st.caption("AI assistant for suspicious account investigation")

# --------------------------------------------------
# DASHBOARD SUMMARY
# --------------------------------------------------

try:
    summary = requests.get(
        f"{API_URL}/summary",
        timeout=5
    ).json()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Transactions",
        summary["total_transactions"]
    )

    c2.metric(
        "Accounts",
        summary["total_accounts"]
    )

    c3.metric(
        "High Risk",
        summary["high_risk_accounts"]
    )

    c4.metric(
        "Suspicious",
        summary["suspicious_accounts"]
    )

except Exception:
    st.error(
        "Cannot connect to FastAPI. "
        "Make sure the backend is running on port 8000."
    )
    st.stop()


st.divider()

# --------------------------------------------------
# ACCOUNT INVESTIGATION
# --------------------------------------------------

st.subheader("Ask the Copilot")

account_id = st.text_input(
    "Enter Account ID",
    placeholder="Example: 8014C7B60"
)

if st.button("Investigate", type="primary"):

    if not account_id.strip():
        st.warning("Please enter an Account ID.")

    else:

        # ------------------------------------------
        # RISK DATA
        # ------------------------------------------

        data = requests.get(
            f"{API_URL}/risk/{account_id}",
            timeout=10
        ).json()

        if "error" in data:

            st.error("Account not found")

        else:

            st.success("Investigation completed")

            # --------------------------------------
            # RISK METRICS
            # --------------------------------------

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Risk Score",
                data["Risk_Score"]
            )

            col2.metric(
                "Risk Level",
                data["Risk_Level"]
            )

            col3.metric(
                "Suspicious",
                data["Suspicious_Flag"]
            )

            # --------------------------------------
            # COPILOT EXPLANATION
            # --------------------------------------

            st.subheader("Copilot Explanation")

            reasons = str(
                data.get("Risk_Reasons", "")
            )

            if reasons == "nan" or reasons.strip() == "":
                st.write(
                    "No strong suspicious reason detected."
                )
            else:

                for reason in reasons.split(";"):
                    if reason.strip():
                        st.write(
                            "•",
                            reason.strip()
                        )

            # --------------------------------------
            # DETECTED PATTERNS
            # --------------------------------------

            st.subheader("Detected Patterns")

            p1, p2, p3 = st.columns(3)

            p1.metric(
                "Smurfing",
                data.get("Smurfing_Flag", "N/A")
            )

            p2.metric(
                "Mule Account",
                data.get("Mule_Flag", "N/A")
            )

            p3.metric(
                "Known Laundering",
                data.get(
                    "Known_Laundering_Account",
                    "N/A"
                )
            )

            # --------------------------------------
            # NEO4J TRANSACTION GRAPH
            # --------------------------------------

            st.subheader(
                "Transaction Network"
            )

            graph_response = requests.get(
                f"{API_URL}/graph/{account_id}",
                timeout=10
            )

            if graph_response.status_code == 200:

                graph_data = graph_response.json()

                nodes = graph_data.get(
                    "nodes",
                    []
                )

                relationships = graph_data.get(
                    "relationships",
                    []
                )

                if nodes:

                    graph_rows = []

                    for relationship in relationships:

                        graph_rows.append({
                            "From": relationship["source"],
                            "To": relationship["target"],
                            "Amount": relationship["amount"]
                        })

                    if graph_rows:

                        graph_df = pd.DataFrame(
                            graph_rows
                        )

                        st.dataframe(
                            graph_df,
                            use_container_width=True,
                            hide_index=True
                        )

                        st.caption(
                            f"Connected accounts found: "
                            f"{len(nodes)}"
                        )

                    else:

                        st.info(
                            "No transaction relationships "
                            "found for this account."
                        )

                else:

                    st.info(
                        "No connected transaction accounts found."
                    )

            else:

                st.warning(
                    "Unable to retrieve transaction network."
                )

            # --------------------------------------
            # AML REPORT
            # --------------------------------------

            st.subheader(
                "Generated AML Report"
            )

            recommendation = (
                "Escalate for manual AML review."
                if data["Suspicious_Flag"]
                else
                "Continue monitoring."
            )

            report = f"""
AML INVESTIGATION REPORT

Account ID: {data['Account']}

Risk Score: {data['Risk_Score']}/100
Risk Level: {data['Risk_Level']}

Summary:
This account was analyzed using transaction behavior,
laundering labels, and suspicious activity indicators.

Reasons:
{data['Risk_Reasons']}

Red Flags:
- Smurfing Pattern: {data['Smurfing_Flag']}
- Mule Account Behavior: {data['Mule_Flag']}
- Known Laundering Account: {data['Known_Laundering_Account']}
- Suspicious Flag: {data['Suspicious_Flag']}

Recommendation:
{recommendation}
"""

            st.text_area(
                "Report",
                report,
                height=350
            )

            # --------------------------------------
            # DOWNLOAD REPORT
            # --------------------------------------

            st.download_button(
                label="Download AML Report",
                data=report,
                file_name=f"AML_Report_{account_id}.txt",
                mime="text/plain"
            )


# --------------------------------------------------
# HIGH RISK ACCOUNTS
# --------------------------------------------------

st.divider()

st.subheader("High Risk Accounts")

high_risk_response = requests.get(
    f"{API_URL}/high-risk",
    timeout=10
)

if high_risk_response.status_code == 200:

    high_risk = high_risk_response.json()

    if high_risk:

        high_risk_df = pd.DataFrame(
            high_risk
        )

        st.dataframe(
            high_risk_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No high-risk accounts found."
        )