import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import requests
from frontend.views import login, upload_hub, analytics

st.set_page_config(page_title="AI Resume Screener", layout="wide")

API_URL = "https://ai-resume-screener-saas.onrender.com"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "token" not in st.session_state:
    st.session_state["token"] = None
if "current_job_id" not in st.session_state:
    st.session_state["current_job_id"] = None

if not st.session_state["logged_in"]:
    login.render()
else:
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to", ["Upload Hub", "Analytics Dashboard"], key="sidebar_nav_radio")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Job Management")
    
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    jobs_res = requests.get(f"{API_URL}/jobs/", headers=headers)
    
    jobs = jobs_res.json() if jobs_res.status_code == 200 else []
    job_options = {job["title"]: job["id"] for job in jobs}
    
    selected_job_title = st.sidebar.selectbox("Select Active Job", options=list(job_options.keys()) if job_options else ["No Jobs Found"], key="sidebar_select_active_job")
    
    if job_options:
        st.session_state["current_job_id"] = job_options[selected_job_title]
        
    with st.sidebar.expander("Create New Job"):
        new_title = st.text_input("Job Title", key="sidebar_new_job_title")
        new_desc = st.text_area("Job Description", key="sidebar_new_job_desc")
        if st.button("Save Job", key="sidebar_save_job_btn"):
            create_res = requests.post(f"{API_URL}/jobs/", json={"title": new_title, "description": new_desc}, headers=headers)
            if create_res.status_code == 200:
                st.success("Job created successfully!")
                st.rerun()
            else:
                st.error("Failed to create job.")

    if choice == "Upload Hub":
        upload_hub.render()
    elif choice == "Analytics Dashboard":
        analytics.render()
        
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", key="sidebar_logout_btn"):
        st.session_state["logged_in"] = False
        st.session_state["token"] = None
        st.session_state["current_job_id"] = None
        st.rerun()