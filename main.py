import json
import streamlit as st
from datetime import datetime
from crewai import Agent, Task, Crew
from openai import OpenAI

# Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- SETUP OPENAI CLIENT ---
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# --- FIXED GOOGLE CREDS LOADING ---
creds_dict = dict(st.secrets["gcp_service_account"])
if "\\n" in creds_dict["private_key"]:
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
creds_json = json.loads(json.dumps(creds_dict))
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)

# --- FUNCTION TO RUN AGENTS ---
def run_compliance_agents(name, id_number, country, is_accredited, offering):
    # Define agents
    kyc_agent = Agent(
        role="KYC Specialist",
        goal="Verify the investor's identity and simulate KYC status",
        backstory="You handle KYC checks in a fast, simulated environment.",
        verbose=False
    )

    compliance_agent = Agent(
        role="Compliance Officer",
        goal="Write a professional compliance note",
        backstory="You summarize KYC and regulatory observations in a memo.",
        verbose=False
    )

    reg_agent = Agent(
        role="Regulatory Analyst",
        goal="Determine eligibility under Reg D or Reg S",
        backstory="You interpret basic inputs to simulate investor eligibility.",
        verbose=False
    )

    legal_agent = Agent(
        role="Legal Drafter",
        goal="Write a legal summary for investor agreements",
        backstory="You translate compliance and regulatory outputs into a clean legal memo.",
        verbose=False
    )

    # Define tasks
    task1 = Task(
        description=f"Perform a KYC check for investor {name} with ID {id_number}. Return status: approved, flagged, or pending.",
        agent=kyc_agent,
        expected_output="approved, flagged, or pending",
        return_value=True
    )

    task2 = Task(
        description=f"Based on the KYC status, write a formal compliance note for investor {name}.",
        agent=compliance_agent,
        expected_output="Professional compliance note.",
        return_value=True
    )

    task3 = Task(
        description=f"Investor {name} is from {country}, is {'' if is_accredited == 'yes' else 'not '}accredited, and applying under {offering}. Determine if they are eligible under Reg D or Reg S.",
        agent=reg_agent,
        expected_output="Regulatory eligibility explanation",
        return_value=True
    )

    task4 = Task(
        description=f"Write a legal memo summarizing investor {name}'s KYC and regulation status for inclusion in a subscription agreement.",
        agent=legal_agent,
        expected_output="Legal summary paragraph",
        return_value=True
    )

    # Run crew
    crew = Crew(agents=[kyc_agent, compliance_agent, reg_agent, legal_agent], tasks=[task1, task2, task3, task4], verbose=False)
    crew.kickoff()

    # Extract results
    kyc_result = task1.output.result
    compliance_note = task2.output.result
    reg_memo = task3.output.result
    legal_memo = task4.output.result

    # Optional: Log to Google Sheet
    try:
        gc = gspread.authorize(creds)
        sheet = gc.open("TokenComply Log").sheet1
        row = [
            name,
            id_number,
            country,
            is_accredited,
            offering,
            kyc_result,
            compliance_note,
            reg_memo,
            legal_memo,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        sheet.append_row(row)
    except Exception as e:
        st.error(f"📄 Google Sheets logging failed: {e}")
        print("📄 Google Sheets logging failed:", e)

    return kyc_result, compliance_note, reg_memo, legal_memo
