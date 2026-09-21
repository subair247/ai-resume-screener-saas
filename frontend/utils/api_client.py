import requests

BASE_URL = "http://localhost:8000"

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data={"username": email, "password": password})
    return response

def register_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    return response

def upload_resume(file):
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{BASE_URL}/upload/resume", files=files)
    return response

def match_candidates(title, description):
    response = requests.post(f"{BASE_URL}/screening/match", json={"title": title, "description": description})
    return response