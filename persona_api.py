# persona_api.py

import requests
import streamlit as st
import uuid

PERSONA_API_KEY = st.secrets["persona"]["api_key"]
TEMPLATE_ID = st.secrets["persona"]["template_id"]
PERSONA_API_URL = "https://withpersona.com/api/v1/inquiries"
HEADERS = {
    "Authorization": f"Bearer {PERSONA_API_KEY}",
    "Content-Type": "application/json"
}

def create_inquiry(name, email):
    headers = {
        "Authorization": f"Bearer {PERSONA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "data": {
            "type": "inquiry",
            "attributes": {
                "template_id": TEMPLATE_ID,
                "reference_id": str(uuid.uuid4()),
                "fields": {
                    "name": name,
                    "email_address": email
                }
            }
        }
    }

    response = requests.post(PERSONA_API_URL, json=payload, headers=headers)

    if response.status_code == 201:
        inquiry_id = response.json()["data"]["id"]
        return inquiry_id
    else:
        st.error("❌ Failed to create inquiry.")
        st.json(response.json())
        return None
        
def check_inquiry_status(inquiry_id):
    url = f"https://withpersona.com/api/v1/inquiries/{inquiry_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()
