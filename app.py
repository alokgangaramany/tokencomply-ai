import streamlit as st
from datetime import datetime
from main import run_compliance_agents # you'll define this in main.py

st.set_page_config(page_title="TokenComply AI", layout="centered")
st.title("🧠 TokenComply AI Onboarding")

with st.form("investor_form"):
    name = st.text_input("Investor Name")
    id_number = st.text_input("ID Number")
    country = st.text_input("Country (e.g., US, India)")
    accredited = st.radio("Is the investor accredited?", ["yes", "no"])
    offering = st.selectbox("Offering Type", ["RegD", "RegS"])

    submitted = st.form_submit_button("Run Compliance Agents")

if submitted:
    with st.spinner("Running agentic compliance checks..."):
        try:
            kyc, compliance, reg, legal = run_compliance_agents(
                name, id_number, country, accredited, offering
            )

            st.success("✅ Agents completed.")
            st.subheader("KYC Result")
            st.write(kyc)

            st.subheader("Compliance Note")
            st.write(compliance)

            st.subheader("Regulatory Memo")
            st.write(reg)

            st.subheader("Legal Memo")
            st.write(legal)

            st.caption(f"Logged on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
