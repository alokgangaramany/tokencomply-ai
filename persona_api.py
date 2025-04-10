# persona_api.py

import requests
import streamlit as st

PERSONA_API_KEY = st.secrets["persona"]["api_key"]
TEMPLATE_ID = st.secrets["persona"]["template_id"]
HEADERS = {
    "Authorization": f"Bearer {PERSONA_API_KEY}",
    "Content-Type": "application/json"
}

def create_inquiry(name, email):
    url = "https://withpersona.com/api/v1/inquiries"
    payload = {
        "data": {
            "type": "inquiry",
            "attributes": {
                "template_id": TEMPLATE_ID,
                "environment": "sandbox",
                "prefill": {
                    "name": name,
                    "email": email
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)
    if response.status_code == 201:
        return response.json()["data"]["id"]
    else:
        st.error(f"❌ Failed to create inquiry.\n\n{response.text}")
        return None
        
def check_inquiry_status(inquiry_id):
    url = f"https://withpersona.com/api/v1/inquiries/{inquiry_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()
