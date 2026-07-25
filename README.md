# T.A.R.A - AI Tactical Strategy Agent 🛡️
> **O2I Defense War Mission Simulator | Automated Military Battle Planning Engine**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-red?style=for-the-badge&logo=streamlit)](https://project-tara-app.streamlit.app/)

👉 **Live Web App Shareable Link:** [https://project-tara-app.streamlit.app/](https://project-tara-app.streamlit.app/)

T.A.R.A (Tactical AI Strategy Agent) is an advanced defense battle simulation assistant built on the O2I Framework. It analyzes user-provided battlefield scenarios, operational assets, and environmental conditions to generate classified, structured military engagement strategies, spatial routes (MGRS coordinates), electronic warfare allocations (Radars, IFF, ESM, CSM), and contingency alternatives.

---

## 🌟 Key Features

- **Multi-Engine AI Routing**: Native support for **Google Gemini (`gemini-3.6-flash`)** and **Groq (`llama-3.3-70b-versatile`)**.
- **Offline Rule Engine Fallback**: Fallback to an offline tactical rule engine if live LLM APIs are unconfigured or unavailable.
- **O2I Framework Terminology Enforcement**: Strict enforcement of Blue Team (friendly) vs. Red Team (hostile), MGRS coordinates, Threat Zones, and EW sensor suites.
- **Interactive Metric Dashboard**: Real-time visualization of Mission Victory Prognosis, Force Balance Ratios, Threat Levels, and AI Model telemetry.
- **Downloadable Classified Dossiers**: Automated export of complete mission dossiers as standardized `.md` files.

---

## 🚀 Quick Start Guide (Run Locally)

Follow these simple steps to run **Project T.A.R.A** locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/hvsharsh/project-T.A.R.A.git
cd project-T.A.R.A
```

### 2. Create and Activate a Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in the root directory (or enter API keys directly in the app sidebar):
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```
> *Note: If no API keys are provided, the simulator automatically operates under the **O2I Offline Tactical Rule Engine**.*

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```

Your browser will automatically open at `http://localhost:8501`.

---

## 📂 Project Structure

```text
project-T.A.R.A/
├── app.py                  # Main Streamlit UI & Interactive Dashboard
├── ai_engine.py            # Core AI Tactical Strategy Engine & LLM API Handlers
├── report_generator.py     # Military Dossier & Markdown Report Generator
├── requirements.txt        # Python package dependencies
├── .env                    # Environment secrets (ignored by Git)
├── .gitignore              # Git file exclusion rules
└── README.md               # Project documentation
```

---

## 📋 Simulator Specs & O2I Terminology

| Component | Specification |
| :--- | :--- |
| **Team Designation** | **Blue Team** (Friendly Forces) vs. **Red Team** (Hostile Forces) |
| **Operational Coordinates** | **MGRS Coordinates** (e.g., `31U DQ 48215 19432`) + Threat Zone Radii |
| **Sensor & EW Suites** | **Radars**, **IFF** (Mode 5 Level 2), **ESM** (Passive RF), **CSM** (COMINT/DF) |
| **Tactical Directives** | **Formation Type**, **Engagement Policy**, **Detection Mode** |

---

## 📄 License
This project is developed for defense war mission simulation research under the O2I Framework.
