import streamlit as st
import json
from openai import OpenAI
from crewai import Agent, Task, Crew
from oauth2client.service_account import ServiceAccountCredentials

# Load OpenAI API Key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)


# Load and sanitize creds from Streamlit Secrets
raw_creds = dict(st.secrets["gcp_service_account"])

# Fix: Convert double backslashes to actual newlines in private_key
raw_creds["private_key"] = raw_creds["private_key"].replace("\\n", "\n")

# Convert to JSON-like object
creds_json = json.loads(json.dumps(raw_creds))

# Use it
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)


# 🚀 MAIN FUNCTION CALLED BY app.py
import streamlit as st
import json
from openai import OpenAI
from crewai import Agent, Task, Crew
from oauth2client.service_account import ServiceAccountCredentials

# Load OpenAI API Key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# Load Google Service Account credentials from Streamlit secrets
creds_dict = dict(st.secrets["gcp_service_account"])
creds_json = json.loads(json.dumps(creds_dict))  # Convert to JSON-like format

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)


# 🚀 MAIN FUNCTION CALLED BY app.py
def run_compliance_agents(name, id_number, country, is_accredited, offering):
    # 1️⃣ Define Agents
    kyc_agent = Agent(
        role="KYC Specialist",
        goal="Verify the investor’s identity and risk status",
        backstory="You handle investor identity checks and simulate KYC outcomes.",
        verbose=True
    )

    compliance_agent = Agent(
        role="Compliance Officer",
        goal="Write a compliance note explaining investor status and next steps",
        backstory="You provide a formal compliance assessment based on KYC status.",
        verbose=True
    )

    reg_agent = Agent(
        role="Regulatory Advisor",
        goal="Determine investor eligibility under Reg D or Reg S",
        backstory="You match investors with applicable US securities regulations.",
        verbose=True
    )

    legal_agent = Agent(
        role="Legal Document Drafter",
        goal="Generate a legal summary memo for the investor's subscription agreement",
        backstory="You draft professional legal memos based on compliance decisions.",
        verbose=True
    )

    # 2️⃣ Define Tasks with return_value=True
    task1 = Task(
        description=f"Perform a KYC check for investor {name} with ID {id_number}. Return status: approved, flagged, or pending.",
        agent=kyc_agent,
        expected_output="approved, flagged, or pending",
        return_value=True
    )

    task2 = Task(
        description=f"Based on the KYC status, write a formal compliance note for investor {name}.",
        agent=compliance_agent,
        expected_output="A 2-3 sentence professional compliance summary.",
        return_value=True
    )

    task3 = Task(
        description=f"Investor {name} is from {country}, is {'accredited' if is_accredited == 'yes' else 'non-accredited'}, and is applying under {offering}. Determine if they are eligible under Reg D or Reg S and explain why.",
        agent=reg_agent,
        expected_output="Eligibility explanation with regulatory reasoning.",
        return_value=True
    )

    task4 = Task(
        description=f"Write a legal memo suitable for a subscription agreement. Investor: {name}, ID: {id_number}, Country: {country}, Accredited: {is_accredited}, Offering: {offering}. Summarize KYC and regulatory findings.",
        agent=legal_agent,
        expected_output="A formal legal summary paragraph for inclusion in investment documents.",
        return_value=True
    )

    # 3️⃣ Create and Run the Crew
    crew = Crew(
        agents=[kyc_agent, compliance_agent, reg_agent, legal_agent],
        tasks=[task1, task2, task3, task4],
        verbose=False
    )

    crew.kickoff()

    # 4️⃣ Extract Outputs
    kyc_result = str(task1.output)
    compliance_note = str(task2.output)
    reg_memo = str(task3.output)
    legal_memo = str(task4.output)

    return kyc_result, compliance_note, reg_memo, legal_memo

# Setup Google Sheets connection
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("TokenComply Log").sheet1  # Your sheet name


# Insert the row
    row = [
         name,
         id_number,
         country,
         is_accredited,
         offering,
         kyc_result,  # KYC output
         compliance_note,  # Compliance note
         reg_memo,  # Reg memo
         legal_memo,  # Legal memo
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     ]

     sheet.append_row(row)
