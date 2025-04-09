import time
import hmac
import hashlib
import base64
import requests
import streamlit as st
from urllib.parse import urlencode
import os
import streamlit as st
import os

SUMSUB_APP_TOKEN = os.getenv("SUMSUB_APP_TOKEN", st.secrets["sumsub"]["app_token"])
SUMSUB_SECRET_KEY = os.getenv("SUMSUB_SECRET_KEY", st.secrets["sumsub"]["secret_key"])
API_BASE = "https://api.sumsub.com"

def create_signature(secret_key, endpoint, method="POST", ts=None):
    if not ts:
        ts = str(int(time.time()))
    string_to_sign = ts + method + endpoint
    digest = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode(), ts

def generate_kyc_link(user_id):
    endpoint = f"/resources/applicants?levelName=basic-kyc-level"
    signature, ts = create_signature(SUMSUB_SECRET_KEY, endpoint, "POST")
    
    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts,
        "Content-Type": "application/json"
    }
    
    body = {
        "externalUserId": user_id
    }

    response = requests.post(API_BASE + endpoint, headers=headers, json=body)

    if response.status_code == 200:
        return f"https://web-sdk.sumsub.com/check-in?accessToken={response.json()['token']}&externalUserId={user_id}"
    else:
        print("❌ Sumsub API Error:", response.status_code, response.text)
        return None

    # Generate the WebSDK link
    link_url = f"/resources/applicants/{user_id}/websdk/link"
    sig, ts = create_signature(SUMSUB_SECRET_KEY, link_url, "POST")
    headers["X-App-Access-Sig"] = sig
    headers["X-App-Access-Ts"] = ts

    link_resp = requests.post(API_BASE + link_url, headers=headers)
    if link_resp.status_code == 200:
        return link_resp.json().get("url")
    else:
        st.error("Failed to get WebSDK link")
        return None

def check_kyc_status(user_id: str):
    endpoint = f"/resources/applicants/{user_id}/requiredIdDocsStatus"
    sig, ts = create_signature(SUMSUB_SECRET_KEY, endpoint, "GET")
    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": sig,
        "X-App-Access-Ts": ts
    }
    response = requests.get(API_BASE + endpoint, headers=headers)
    if response.status_code == 200:
        review = response.json()
        return review.get("reviewStatus", "unknown")
    else:
        return "error"
