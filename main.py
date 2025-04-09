import os
from openai import OpenAI
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Load the API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Simulated KYC database
kyc_database = {
    "12345": "approved",
    "67890": "flagged",
    "11111": "pending"
}

def check_kyc_status(id_number):
    return kyc_database.get(id_number, "not found")

def generate_compliance_note(name, id_number, status):
    prompt = f"""
You are a compliance officer. An investor named {name} submitted ID {id_number}.
The KYC status returned: {status}.

Write a 2-sentence compliance decision note explaining what this status means and what the next action should be.
Keep it professional.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# Ask for user input



# name = input("Enter investor name: ")
# id_number = input("Enter ID number: ")
# status = check_kyc_status(id_number)

#print(f"\n--- KYC CHECK ---")
#print(f"Name: {name}")
#print(f"ID: {id_number}")
#print(f"Status: {status.upper()}")

#note = generate_compliance_note(name, id_number, status)
#print(f"\n📝 Compliance Note:\n{note}")

# country = input("Enter investor country (e.g., US, UK, India): ")
#is_accredited = input("Is the investor accredited? (yes/no): ").lower()
#offering_type = input("Offering type (RegD/RegS): ").upper()

def determine_eligibility(country, is_accredited, offering_type):
    prompt = f"""
You are a compliance AI agent.

The investor is from {country}. They are {'an accredited' if is_accredited == 'yes' else 'a non-accredited'} investor.
The offering is being conducted under {offering_type}.

Please:
- Decide if the investor is eligible for the offering
- Explain why
- Recommend next steps

Use formal compliance language.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


def generate_subscription_agreement(name, id_number, status):
    prompt = f"""
You are a legal assistant generating a subscription agreement summary for an investor.

Investor Details:
- Name: {name}
- ID Number: {id_number}
- KYC Status: {status}

Write a short legal-style summary suitable for inclusion in a subscription agreement, explaining their compliance status and eligibility for tokenized asset purchase under Reg D.
Use formal language.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

# Generate the legal memo
# legal_doc = generate_subscription_agreement(name, id_number, status)

# print(f"\n📄 Legal Memo:\n{legal_doc}")

#reg_result = determine_eligibility(country, is_accredited, offering_type)
#print(f"\n⚖️ Regulatory Eligibility Memo:\n{reg_result}")

# Define Agents

kyc_agent = Agent(
    role="KYC Specialist",
    goal="Verify the investor’s identity and risk status",
    backstory="You are responsible for checking ID numbers and simulating basic KYC results.",
    verbose=True
)

compliance_agent = Agent(
    role="Compliance Officer",
    goal="Write a compliance note explaining the investor's status and next steps",
    backstory="You analyze the investor’s KYC result and suggest action in legal language.",
    verbose=True
)

reg_agent = Agent(
    role="Regulatory Advisor",
    goal="Determine eligibility under Reg D or Reg S based on investor info",
    backstory="You evaluate the investor's jurisdiction and accreditation status to determine the appropriate offering framework.",
    verbose=True
)

legal_agent = Agent(
    role="Legal Document Drafter",
    goal="Generate a subscription agreement summary based on compliance info",
    backstory="You are a legal assistant responsible for preparing formal investor documentation. You specialize in translating compliance data into proper legal memos.",
    verbose=True
)


# Inputs (pretend user flow)
name = input("Enter investor name: ")
id_number = input("Enter ID number (try 12345 or 67890): ")
country = input("Enter country: ")
is_accredited = input("Is the investor accredited? (yes/no): ").lower()
offering = input("Offering type (RegD/RegS): ").upper()

# Define Tasks

task1 = Task(
    description=f"Simulate a KYC check for investor {name} with ID {id_number}. Check if ID is 'approved', 'flagged', or 'pending'.",
    agent=kyc_agent,
    expected_output="A single word output: approved, flagged, pending, or not found.",
    return_value=True
)

task2 = Task(
    description=f"Based on the KYC result for {name}, write a short compliance note explaining the status.",
    agent=compliance_agent,
    expected_output="A 2-3 sentence compliance note in formal tone.",
    return_value=True
)

task3 = Task(
    description=f"The investor is from {country}, {'accredited' if is_accredited == 'yes' else 'non-accredited'}, and the offering is under {offering}. Determine if they are eligible under Reg D or Reg S and explain why.",
    agent=reg_agent,
    expected_output="A regulatory eligibility summary with next steps.",
    return_value=True
)

task4 = Task(
    description=f"""Create a legal memo for investor {name} (ID: {id_number}) from {country}, who is {'accredited' if is_accredited == 'yes' else 'non-accredited'}, and is applying under {offering}.

Write a legal-style paragraph suitable for use in a subscription agreement. Summarize their KYC status and regulatory eligibility for tokenized securities.""",
    agent=legal_agent,
    expected_output="A professional legal memo paragraph suitable for inclusion in formal investment documentation.",
    return_value=True
)

# Launch Crew
crew = Crew(
    agents=[kyc_agent, compliance_agent, reg_agent, legal_agent],
    tasks=[task1, task2, task3, task4],
    verbose=True
)

result = crew.kickoff()


kyc_result = str(task1.output)
compliance_note = str(task2.output)
reg_memo = str(task3.output)
legal_memo = str(task4.output)



def run_compliance_agents(name, id_number, country, is_accredited, offering):
    # Your agent/task setup code goes here as before

    # Run the crew
    crew.kickoff()

    # Extract outputs
    kyc = str(task1.output)
    compliance = str(task2.output)
    reg = str(task3.output)
    legal = str(task4.output)

    return kyc, compliance, reg, legal

#print("\n🧠 DEBUG: Crew result type:", type(result))
#print("🧠 DEBUG: Crew result value:", result)

print("\n✅ Final Multi-Agent Output:")
print(result)

# Setup Google Sheets connection
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("TokenComply Log").sheet1  # Your sheet name

#outputs = result.split('\n\n')  # crude splitter — or parse better later
#outputs = result.final_output.split('\n\n')
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

