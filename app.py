import streamlit as st
from datetime import datetime
from main import run_compliance_agents
# from kyc_api import generate_kyc_link, check_kyc_status
# from persona_api import create_inquiry, check_inquiry_status
import time
import urllib.parse
from persona_api import generate_persona_flow_url 

PERSONA_API_KEY = st.secrets["persona"]["api_key"]
TEMPLATE_ID = st.secrets["persona"]["template_id"]

st.set_page_config(page_title="TokenComply AI", layout="centered")
st.title("🧠 TokenComply AI Onboarding")

use_real_kyc = st.checkbox("🔐 Use real KYC via Persona")



with st.form("investor_form"):
    name = st.text_input("Investor Name")
    email = st.text_input("Email Address") 
    id_number = st.text_input("ID Number")
    country = st.text_input("Country (e.g., US, India)")
    accredited = st.radio("Is the investor accredited?", ["yes", "no"])
    offering = st.selectbox("Offering Type", ["RegD", "RegS"])

    submitted = st.form_submit_button("Run Compliance Agents")

if submitted:
    if use_real_kyc:
    with st.spinner("🔗 Generating KYC verification link..."):
        kyc_url = generate_persona_url(TEMPLATE_ID, name, email)
        st.success("✅ KYC verification ready")
        st.markdown(f"[Click here to verify →]({kyc_url})", unsafe_allow_html=True)
        st.markdown("#### Or complete verification below:")
        st.components.v1.iframe(kyc_url, height=600)
           
            else:
                st.error("❌ Failed to create inquiry.")
    else:
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
                st.error(f"❌ An error occurred: {e}")

# if submitted:
#     if use_real_kyc:
#         st.info("🔍 Creating applicant and starting KYC process...")
#         try:
#             kyc_link = generate_kyc_link(id_number)
#             st.success("✅ KYC link generated. Please complete verification:")
#             st.markdown(f"[Click here to complete KYC]({kyc_link})")

#             with st.spinner("⏳ Waiting for KYC approval (up to 30 seconds)..."):
#                 MAX_WAIT = 30
#                 start = time.time()
#                 status = check_kyc_status(id_number)

#                 while status != "approved" and (time.time() - start < MAX_WAIT):
#                     time.sleep(2)
#                     status = check_kyc_status(id_number)

#                 if status == "approved":
#                     st.success("✅ KYC Approved. Proceeding to compliance checks...")
#                 else:
#                     st.warning(f"⏳ KYC still `{status}`. Please try again later.")
#                     st.stop()

#         except Exception as e:
#             st.error(f"❌ Failed to create applicant or check status: {e}")
#             st.stop()

#     with st.spinner("⚙️ Running agentic compliance checks..."):
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
#             st.error(f"An error occurred during compliance checks: {e}")


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
