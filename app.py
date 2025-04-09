import streamlit as st
from datetime import datetime
from main import run_compliance_agents # you'll define this in main.py

from kyc_api import generate_kyc_link, check_kyc_status

st.title("🧠 TokenComply AI Onboarding")
use_real_kyc = st.checkbox("🔐 Use real KYC via Sumsub")

with st.form("investor_form"):
    name = st.text_input("Investor Name")
    id_number = st.text_input("ID Number (used as KYC ID)")
    country = st.text_input("Country (e.g., US)")
    accredited = st.radio("Is the investor accredited?", ["yes", "no"])
    offering = st.selectbox("Offering Type", ["RegD", "RegS"])
    submitted = st.form_submit_button("Submit")

if submitted:
    if use_real_kyc:
        link = generate_kyc_link(id_number)
        if link:
            st.success("✅ KYC link created!")
            st.markdown(f"[Click to complete verification →]({link})", unsafe_allow_html=True)
            st.info("Come back and click below to continue once KYC is completed.")
            st.session_state["kyc_user_id"] = id_number
            st.session_state["kyc_info"] = (name, id_number, country, accredited, offering)
    else:
        # run directly with simulated KYC
        with st.spinner("Running agents with simulated KYC..."):
            kyc, compliance, reg, legal = run_compliance_agents(name, id_number, country, accredited, offering)
            st.success("✅ Agents done.")
            st.write_outputs(kyc, compliance, reg, legal)

# 🧪 Check KYC Status
if "kyc_user_id" in st.session_state:
    st.subheader("✅ Check KYC Status and Continue")
    if st.button("Check Status + Run Agents"):
        status = check_kyc_status(st.session_state["kyc_user_id"])
        st.write(f"KYC Status: `{status}`")
        if status == "completed":
            name, id_number, country, accredited, offering = st.session_state["kyc_info"]
            with st.spinner("Running agents with real KYC approval..."):
                kyc, compliance, reg, legal = run_compliance_agents(name, id_number, country, accredited, offering)
                st.success("✅ All done.")
                st.write_outputs(kyc, compliance, reg, legal)
        elif status == "pending":
            st.warning("KYC is still pending. Please wait and try again.")
        else:
            st.error("Something went wrong. Please retry or contact support.")


def st_write_outputs(kyc, compliance, reg, legal):
    st.subheader("KYC Result")
    st.write(kyc)
    st.subheader("Compliance Note")
    st.write(compliance)
    st.subheader("Regulatory Memo")
    st.write(reg)
    st.subheader("Legal Memo")
    st.write(legal)


# st.set_page_config(page_title="TokenComply AI", layout="centered")
# st.title("🧠 TokenComply AI Onboarding")

# with st.form("investor_form"):
#     name = st.text_input("Investor Name")
#     id_number = st.text_input("ID Number")
#     country = st.text_input("Country (e.g., US, India)")
#     accredited = st.radio("Is the investor accredited?", ["yes", "no"])
#     offering = st.selectbox("Offering Type", ["RegD", "RegS"])

#     submitted = st.form_submit_button("Run Compliance Agents")

# if submitted:
#     with st.spinner("Running agentic compliance checks..."):
#         try:
#             kyc, compliance, reg, legal = run_compliance_agents(
#                 name, id_number, country, accredited, offering
#             )

#             st.success("✅ Agents completed.")
#             st.subheader("KYC Result")
#             st.write(kyc)

#             st.subheader("Compliance Note")
#             st.write(compliance)

#             st.subheader("Regulatory Memo")
#             st.write(reg)

#             st.subheader("Legal Memo")
#             st.write(legal)

#             st.caption(f"Logged on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#         except Exception as e:
#             st.error(f"An error occurred: {e}")
