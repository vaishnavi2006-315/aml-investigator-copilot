import streamlit as st
from backend.db import get_stats

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