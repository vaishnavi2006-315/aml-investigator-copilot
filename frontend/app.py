import streamlit as st
from backend.db import get_stats, search_account

st.set_page_config(
    page_title="AML Investigator Copilot",
    layout="wide"
)

st.title("🔍 AML Investigator Copilot")

st.write("Welcome to the AML Investigation Dashboard")

st.divider()

col1, col2, col3 = st.columns(3)

accounts, transactions, high_risk = get_stats()

accounts, transactions, high_risk = get_stats()

col1.metric("Accounts", accounts)
col2.metric("Transactions", transactions)
col3.metric("High Risk Accounts", high_risk)

st.header("Investigation Modules")

st.success("✅ Graph Database Connected")
st.success("✅ Risk Detection")
st.success("✅ Multi-Hop Tracing")
st.success("✅ Circular Detection")

st.divider()

st.header("🔎 Search Account")

account = st.text_input("Enter Account ID")

if st.button("Search"):

    if account:

        data = search_account(account)

        if data and data["account"] is not None:

            st.subheader("Account Summary")

            st.write(f"**Account ID:** {data['account']}")
            st.write(f"**Outgoing Transactions:** {data['outgoing']}")
            st.write(f"**Incoming Transactions:** {data['incoming']}")
            st.write(f"**Total Sent:** {data['sent']}")
            st.write(f"**Total Received:** {data['received']}")

        else:
            st.error("Account not found.")

    else:
        st.warning("Please enter an Account ID.")