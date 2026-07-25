# T.A.R.A - AI Tactical Strategy Agent 🛡️

> **Advanced Defense War Mission Simulator | Automated Military Battle Planning Engine (O2I Framework)**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-red?style=for-the-badge&logo=streamlit)](https://project-tara-app.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![AI Models](https://img.shields.io/badge/AI%20Engine-Gemini%20%7C%20Groq-purple.svg?style=for-the-badge)](https://ai.google.dev/)

👉 **Live Web App Shareable Link:** [https://project-tara-app.streamlit.app/](https://project-tara-app.streamlit.app/)

---

## 📌 Overview

**T.A.R.A (Tactical AI Strategy Agent)** is an advanced defense battle simulation and tactical decision-support assistant built for dynamic scenario analysis. Operating under defense war mission simulation protocols (O2I Framework), T.A.R.A evaluates mission briefings, operational assets, force imbalances, and environmental constraints to generate comprehensive military engagement strategies.

Whether planning air defense suppression, coastal infiltration, or armored interdiction, T.A.R.A delivers actionable operational plans, terrain-aware spatial routes (MGRS coordinates), electronic warfare sensor allocations (Radar, IFF, ESM, CSM), risk evaluations, and alternative contingency plans.

---

## 🌟 Key Features

* **🤖 Multi-Engine AI Routing:**
  * Native integration with **Google Gemini (`gemini-3.6-flash`)** and **Groq (`llama-3.3-70b-versatile`)**.
  * Intelligent provider selection ("Auto", "Gemini", "Groq") with automatic fallback logic.
* **🛡️ Offline Rule Engine Fallback:**
  * Seamless fallback to a deterministic offline tactical simulation engine if live LLM APIs are unconfigured or unavailable.
* **⚔️ Strict Tactical Protocols:**
  * Enforces standardized operational doctrine: **Blue Team** (Friendly/Allied) vs. **Red Team** (Hostile).
  * Generates spatial movement routes in standard **MGRS coordinates** with elevation and threat buffer radii.
  * Allocates key sensor & Electronic Warfare (EW) suites: **Radars**, **IFF**, **ESM**, and **CSM**.
* **📊 Interactive Metric Dashboard:**
  * Real-time calculation and visualization of Mission Victory Prognosis, Force Balance Ratios, Threat Index, and AI telemetry.
* **📄 Downloadable Classified Dossiers:**
  * One-click export of complete mission dossiers as standardized `.md` Markdown files formatted for post-mission analysis and archival.
* **🎯 Preset Tactical Scenarios:**
  * Built-in sample scenarios (Coastal Defense, Air Defense Suppression, Armored Interdiction) for rapid scenario evaluation.

---

## 🏗️ System Architecture & File Structure

```
project-T.A.R.A/
├── app.py                  # Main Streamlit web application & UI workflow
├── ai_engine.py            # Core AI Tactical Engine (Gemini / Groq / Offline Simulation)
├── report_generator.py     # Military mission dossier generator (.md exporter)
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables configuration (API keys)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

---

## 🚀 Quick Start Guide (Run Locally)

Follow these steps to set up and run **Project T.A.R.A** locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/hvsharsh/project-T.A.R.A.git
cd project-T.A.R.A
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)
```bash
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\activate

# On Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create or edit the `.env` file in the root directory and add your API key(s):

```env
# Optional: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Groq API Key
GROQ_API_KEY=your_groq_api_key_here
```
> **Note:** If no API keys are configured, T.A.R.A automatically runs in **Offline Tactical Simulation Mode**, allowing full offline testing without external API dependencies. API keys can also be provided directly via the web app sidebar.

### 5. Launch the Streamlit Application
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 🎮 How to Use T.A.R.A

1. **Select or Write a Mission Briefing:** Choose a preset scenario from the dropdown menu or enter custom operational text.
2. **Configure Tactical Parameters:** Adjust the Blue Team / Red Team force numbers, threat severity level, and weather/visibility conditions.
3. **Select AI Engine:** Choose your preferred LLM provider (`Auto Select`, `Google Gemini`, `Groq Llama-3.3`, or `Offline Simulation`).
4. **Execute Tactical Analysis:** Click **"Generate Tactical Strategy"** to initiate mission planning.
5. **Review Dossier & Route Data:** Inspect the generated primary strategy, resource allocations, spatial routes (MGRS), risk matrix, and alternative contingency options.
6. **Export Classified Report:** Click **"Download Classified Mission Dossier"** to save a copy of the operational briefing.

---

## ☁️ Deployment

### Deploying to Streamlit Cloud

1. Push your repository to GitHub (`https://github.com/hvsharsh/project-T.A.R.A`).
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3. Click **"New App"** and select your GitHub repository, branch (`main`), and main file path (`app.py`).
4. (Optional) In Advanced Settings, add your `GEMINI_API_KEY` or `GROQ_API_KEY` under **Secrets**.
5. Click **"Deploy"**!

---

## 📜 License & Disclaimer

This project is developed for defense war simulation research and scenario analysis under the O2I Framework. Distributed under the MIT License.

---

<p align="center">
  <b>Developed by Defense AI Engineering Team</b>
</p>