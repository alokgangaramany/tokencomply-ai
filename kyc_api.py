import time
import hashlib
import hmac
import requests
import uuid
import streamlit as st
import json

SUMSUB_APP_TOKEN = st.secrets["sumsub"]["app_token"]
SUMSUB_SECRET_KEY = st.secrets["sumsub"]["secret_key"]
API_BASE = "https://api.sumsub.com"


def sign_request(method, path, body):
    ts = str(int(time.time()))
    string_to_sign = ts + method.upper() + path + body
    signature = hmac.new(
        SUMSUB_SECRET_KEY.encode(),
        string_to_sign.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature, ts


def generate_kyc_link(user_id):
    path = f"/resources/accessTokens?userId={user_id}&levelName=id-and-liveness"
    url = API_BASE + path

    payload = {
        "externalUserId": user_id
    }
    body = json.dumps(payload)

    signature, ts = sign_request("POST", path, body)

    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, data=body)
    data = response.json()

    if response.status_code != 200 or "token" not in data:
        raise Exception(f"Failed to get token: {data}")

    token = data["token"]
    return f"https://web.sumsub.com/idensic/mobile-sdk-link/#/access-token/{token}"


def check_kyc_status(user_id):
    path = f"/resources/applicants/-;externalUserId={user_id}/status"
    url = API_BASE + path
    method = "GET"
    body = ""

    signature, ts = sign_request(method, path, body)

    headers = {
        "X-App-Token": SUMSUB_APP_TOKEN,
        "X-App-Access-Sig": signature,
        "X-App-Access-Ts": ts
    }

    response = requests.get(url, headers=headers)
    return response.json()
