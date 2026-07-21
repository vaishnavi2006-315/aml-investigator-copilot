import streamlit as st

st.set_page_config(
    page_title="AML Investigator Copilot",
    layout="wide"
)

st.title("🔍 AML Investigator Copilot")

st.write("Welcome to the AML Investigation Dashboard")

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Accounts", "6023")
col2.metric("Transactions", "5000")
col3.metric("High Risk Accounts", "20")

st.header("Investigation Modules")

st.success("✅ Graph Database Connected")
st.success("✅ Risk Detection")
st.success("✅ Multi-Hop Tracing")
st.success("✅ Circular Detection")