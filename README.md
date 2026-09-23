# AI Resume Screener SaaS

An enterprise-grade, full-stack AI recruitment platform designed to automate candidate shortlisting, semantic resume ranking, skill gap analysis, targeted technical interview generation, and recruiter email notifications.

---

## 🌐 System Architecture

```mermaid
graph TD
    %% Client Layer
    User[Recruiter / User] -->|HTTPS / Streamlit UI| Frontend[Streamlit Frontend Client]

    %% API Gateway & Load Balancer
    Frontend -->|REST API Requests / JSON| Gateway[Nginx / API Gateway / Load Balancer]

    %% Backend Services Layer
    Gateway -->|FastAPI Application| Backend[FastAPI Backend Server]

    %% Core Processing & AI Pipeline
    subgraph Backend Processing
        Backend -->|Extract Text| Parser[PDF/DOCX Parser Engine]
        Backend -->|Compute Embeddings & FAISS| NLP[NLP & Semantic Matching Pipeline]
        Backend -->|Generate Prompts| LLM[Google Gemini API Engine]
        Backend -->|SMTP Protocol| Email[SMTP Mail Dispatcher Service]
    end

    %% Storage & External Services
    Backend -->|Read/Write Structured Data| DB[(MySQL Relational Database)]
    LLM -->|External HTTPS Call| Gemini[Google Gemini Cloud LLM]
    Email -->|TLS Secure Auth| Gmail[Gmail SMTP Server]
```
---

### 📋 Architecture Components Breakdown
---
1. **Client & Load Balancer Layer (`Streamlit` & `Nginx`):**
   * **Frontend:** Built using Streamlit for fast dashboard prototyping, file uploads, and reactive UI rendering.
   * **API Gateway / Reverse Proxy:** Handles incoming web traffic, SSL termination, and routes HTTP requests securely to backend application instances.

2. **Application & Business Logic Layer (`FastAPI`):**
   * Asynchronous FastAPI server handling concurrent candidate screening requests, routing jobs, managing data payloads, and executing core validation without blocking threads.

3. **AI & NLP Processing Engine (`FAISS` & `Gemini API`):**
   * **Local Processing:** Extracts raw text from uploaded PDF/DOCX files, performs NLP entity extraction using SpaCy, and handles semantic matching efficiently through optimized lightweight vector pipelines and the Gemini API.
   * **Cloud LLM Integration:** Communicates securely via HTTPS with the external Google Gemini API to generate customized technical interview questions based on identified candidate-job skill gaps.

4. **Data Persistence Layer (`MySQL` & `SQLAlchemy`):**
   * Relational database storing structured data including user accounts, job descriptions, candidate metadata, and evaluation metrics via SQLAlchemy ORM mapping.

5. **Notification & Communication Layer (`SMTP`):**
   * Handles asynchronous transactional email dispatches using secure TLS-encrypted socket connections with Gmail's SMTP infrastructure to deliver generated interview guides directly to recruiters.

---
## 🚀 Key Features

* **Bulk Resume Upload & Parsing:** Seamlessly handles multiple PDF and DOCX candidate uploads, extracting structured profile information.
* **Semantic Resume Scoring & Gap Analysis:** Leverages vector embeddings and semantic similarity metrics to score candidates against job descriptions, featuring detailed section-wise breakdowns and missing keyword identification.
* **AI-Powered Interview Question Generator:** Dynamically generates custom, rigorous technical interview prompts tailored to each candidate's unique project history and skill gaps using LLM integration.
* **Automated Recruiter Notifications:** Dispatches structured interview question reports directly to 
hiring managers via a secure SMTP-backed email pipeline.

---
## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI, Python
* **Database & ORM:** MySQL, SQLAlchemy, Pydantic v2
* **AI & NLP:** Gemini API, FAISS, custom semantic matching pipelines
* **Communication:** Python `smtplib` for automated transactional emailing

---
## 💡 Engineering Challenges & Solutions

Recruiters look closely at how developers troubleshoot and resolve real-world architectural bottlenecks. Below are the key challenges encountered during the development of this platform and how they were systematically solved:

### 1. Resolving Authentication Restrictions for Public Demo Workflows
* **The Issue:** The initial backend job routing implementation enforced strict recruiter authentication (`current_user = Depends(get_current_user)`), which resulted in `401 Unauthorized` errors when the Streamlit frontend fetched job listings without stateful session tokens.
* **The Solution:** Refactored the `/jobs/` and job creation routers to streamline public-facing demo accessibility, ensuring seamless data fetching and smooth UI rendering without unnecessary login barriers.

### 2. Pydantic v2 Strict Model Validation & Environment Mismatches
* **The Issue:** Introducing SMTP configuration variables (`MAIL_USERNAME`, `MAIL_PASSWORD`) into the `.env` file triggered strict Pydantic validation errors (`extra_forbidden`) because the backend `Settings` class did not explicitly declare them, nor did it allow extra fields.
* **The Solution:** Updated the `Settings` class in `config.py` to include the required mail variables and configured `class Config` with `extra = "ignore"` to gracefully handle environment variables.

### 3. Google SMTP Authentication & App Passwords Integration
* **The Issue:** Standard Gmail account passwords failed during programmatic SMTP transmission due to Google's strict security protocols and multi-factor authentication requirements.
* **The Solution:** Generated a dedicated 16-digit Google **App Password** via account security settings, stripped accidental whitespace formatting from the environment configuration string, and successfully established secure TLS-encrypted socket communication.

### 4. Gemini API Model Version Deprecations & 404 Errors
* **The Issue:** Outdated LLM endpoint references caused connection failures and `404 Not Found` exceptions during resume screening and interview question generation.
* **The Solution:** Updated the API client configuration to target currently active Google Gemini model versions, restoring stable and instantaneous inference responses.

### 5. Overcoming Render Free Tier RAM Limits (Out of Memory Crashes)
* **The Issue:** Heavy AI libraries like PyTorch and `sentence-transformers` exceeded Render's strict 512MB free tier RAM limit during app startup and execution, causing persistent `Out of Memory (OOM)` container crashes.
* **The Solution:** Implemented lazy-loading for heavy modules (`google.generativeai`), optimized garbage collection (`gc.collect()`), and transitioned to a lightweight embedding fallback architecture to ensure smooth execution well within the 512MB memory boundary.
  
---
## ⚙️ Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/your-username/ai-resume-screener.git](https://github.com/your-username/ai-resume-screener.git)
   cd ai-resume-screener

---
2. **Configure the Environment:**
   Create a `.env` file in the root backend directory and add your credentials:
   ```env
   PROJECT_NAME="AI Resume Screener"
   DATABASE_URL="mysql+pymysql://root:yourpassword@localhost:3306/resume_db"
   SECRET_KEY="your-super-secret-key"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   GEMINI_API_KEY="your-gemini-api-key"
   MAIL_USERNAME="your-email@gmail.com"
   MAIL_PASSWORD="your-16-digit-app-password"

---
3. **Run the Backend Server:**
```bash
uvicorn backend.app.main:app --reload
```

---
4. **Launch the Frontend:**
```bash
streamlit run frontend/app.py
```

------
## 🚀 Live Production Deployment
* **Backend API (Render):** Hosted as a Docker container on Render at `https://ai-resume-screener-saas.onrender.com`
* **Frontend UI (Streamlit Cloud):** Hosted on Streamlit Community Cloud, securely communicating with the FastAPI backend REST endpoints.