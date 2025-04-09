import time
import hmac
import hashlib
import base64
import requests
import streamlit as st
from urllib.parse import urlencode
import os


SUMSUB_APP_TOKEN = st.secrets["sumsub"]["app_token"]
SUMSUB_SECRET_KEY = st.secrets["sumsub"]["secret_key"]
API_BASE = "https://api.sumsub.com"



def generate_kyc_link(user_id):
    app_token = st.secrets["sumsub"]["app_token"]
    secret_key = st.secrets["sumsub"]["secret_key"]

    endpoint = "/resources/applicants?levelName=basic-kyc-level"
    ts = str(int(time.time()))
    string_to_sign = ts + "POST" + endpoint

    signature = base64.b64encode(
        hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    ).decode()

    headers = {
        "X-App-Token": app_token,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts,
        "Content-Type": "application/json"
    }

    body = {"externalUserId": user_id}

    try:
        response = requests.post("https://api.sumsub.com" + endpoint, headers=headers, json=body)
        print("🔍 STATUS:", response.status_code)
        print("🔍 BODY:", response.text)

        if response.status_code == 200:
            token = response.json()["token"]
            return f"https://web-sdk.sumsub.com/check-in?accessToken={token}&externalUserId={user_id}"
        else:
            return None
    except Exception as e:
        print("❌ Exception while creating applicant:", e)
        return None


def check_kyc_status(user_id):
    app_token = st.secrets["sumsub"]["app_token"]
    secret_key = st.secrets["sumsub"]["secret_key"]

    endpoint = f"/resources/applicants/-;externalUserId={user_id}/status"
    ts = str(int(time.time()))
    string_to_sign = ts + "GET" + endpoint

    signature = base64.b64encode(
        hmac.new(secret_key.encode(), string_to_sign.encode(), hashlib.sha256).digest()
    ).decode()

    headers = {
        "X-App-Token": app_token,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts,
    }

    try:
        response = requests.get("https://api.sumsub.com" + endpoint, headers=headers)
        print("📦 KYC STATUS RESPONSE:", response.status_code, response.text)

        if response.status_code == 200:
            return response.json().get("review", {}).get("reviewResult", {}).get("reviewAnswer", "pending")
        else:
            return "error"
    except Exception as e:
        print("❌ Exception while checking status:", e)
        return "error"
