import streamlit as st
import requests

BASE_URL = "https://ai-resume-screener-saas.onrender.com"

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response

def register_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    return response

def upload_resume(file):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        token = st.session_state.get("token")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        response = requests.post(f"{BASE_URL}/upload/resume", files=files, headers=headers)
        return response
    except Exception as e:
        class DummyResponse:
            status_code = 500
            text = str(e)
            def json(self):
                return {"detail": str(e)}
        return DummyResponse()

def match_candidates(title, description):
    try:
        token = st.session_state.get("token")
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.post(f"{BASE_URL}/screening/match", json={"title": title, "description": description}, headers=headers)
        return response
    except Exception as e:
        class DummyResponse:
            status_code = 500
            text = str(e)
            def json(self):
                return {"detail": str(e)}
        return DummyResponse()