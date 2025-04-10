import requests
import json
import streamlit as st

# Load Persona API key from Streamlit secrets
PERSONA_API_KEY = st.secrets["persona"]["api_key"]
TEMPLATE_ID =  st.secrets["persona"]["template_id"]

API_BASE = "https://withpersona.com/api/v1"

def create_inquiry(name, email):
    url = f"{API_BASE}/inquiries"
    headers = {
        "Authorization": f"Bearer {PERSONA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": {
            "type": "inquiry",
            "attributes": {
                "template_id": TEMPLATE_ID
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        data = response.json()
        inquiry_id = data["data"]["id"]
        return inquiry_id
    else:
        st.error("❌ Failed to create inquiry.")
        st.json(response.json())
        return None


def get_inquiry_status(inquiry_id):
    url = f"{API_BASE}/inquiries/{inquiry_id}"
    headers = {
        "Authorization": f"Bearer {PERSONA_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch inquiry status.")
        st.json(response.json())
        return None
