import time
import hashlib
import hmac
import requests
import uuid
import streamlit as st

SUMSUB_APP_TOKEN = st.secrets["sumsub"]["app_token"]
SUMSUB_SECRET_KEY = st.secrets["sumsub"]["secret_key"]
API_BASE = "https://api.sumsub.com"


def sign_request(method, url, body):
    ts = str(int(time.time()))
    string_to_sign = ts + method.upper() + url + body
    signature = hmac.new(SUMSUB_SECRET_KEY.encode(), string_to_sign.encode(), hashlib.sha256).hexdigest()
    return signature, ts


def generate_kyc_link(user_id):
    url = f"{API_BASE}/resources/accessTokens?userId={user_id}&levelName=basic-kyc-level"
    method = "POST"
    body = ""
    signature, ts = sign_request(method, url, body)

    headers = {
        "Content-Type": "application/json",
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    if response.status_code != 200 or "token" not in data:
        raise Exception(f"Failed to get token: {data}")

    token = data["token"]
    return f"https://web.sumsub.com/idensic/mobile-sdk-link/#/access-token/{token}"


def check_kyc_status(user_id):
    url = f"{API_BASE}/resources/applicants/-;externalUserId={user_id}/status"
    method = "GET"
    body = ""
    signature, ts = sign_request(method, url, body)

    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts
    }

    response = requests.get(url, headers=headers)
    return response.json()
