import requests
import streamlit as st

PERSONA_API_KEY = st.secrets["persona"]["api_key"]
HEADERS = {
    "Authorization": f"Bearer {PERSONA_API_KEY}",
    "Content-Type": "application/json"
}

def create_inquiry(name, email):
    url = "https://withpersona.com/api/v1/inquiries"
    data = {
        "data": {
            "type": "inquiry",
            "attributes": {
                "template-id": "itmpl_inWKMrzDKYbePHd3Xy6cMeV9xmcA",  # Optional but recommended
                "name-first": name.split()[0],
                "name-last": name.split()[-1] if len(name.split()) > 1 else "",
                "email-address": email
            }
        }
    }

    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        return response.json()["data"]["id"]
    else:
        st.error("Failed to create inquiry")
        st.write(response.text)
        return None

def check_inquiry_status(inquiry_id):
    url = f"https://withpersona.com/api/v1/inquiries/{inquiry_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()
