import time
import hmac
import hashlib
import base64
import requests
import streamlit as st

SUMSUB_APP_TOKEN = st.secrets["sumsub"]["app_token"]
SUMSUB_SECRET_KEY = st.secrets["sumsub"]["secret_key"]
API_BASE = "https://api.sumsub.com"

def create_signature(secret_key, url, method):
    ts = str(int(time.time()))
    string_to_sign = f"{ts}{method.upper()}{url}"
    digest = hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode(), ts

def generate_kyc_link(user_id: str):
    level_name = "basic-kyc-level"
    create_url = f"/resources/applicants?levelName={level_name}"
    sig, ts = create_signature(SUMSUB_SECRET_KEY, create_url, "POST")
    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": sig,
        "X-App-Access-Ts": ts,
        "Content-Type": "application/json"
    }
    body = {"externalUserId": user_id}

    create_resp = requests.post(API_BASE + create_url, json=body, headers=headers)
    if create_resp.status_code != 200:
        st.error("Failed to create applicant")
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
