"""
app.py

Main Streamlit Application for AI Tactical Strategy Agent (project T.A.R.A)
for Defense War Mission Simulator (Tactical AI Framework).

Features:
- 100% native Streamlit components (clean, minimalist layout)
- Preserved widget session state persistence across reruns
- Synchronized preset scenario selection & text area binding
- Input validation for mission briefing scenarios
- Comprehensive error diagnostics surfacing for API failures
- Downloadable classified military dossiers

Author: Lead AI Engineer & Senior UI Developer
Version: 2.4.0
"""

import os
import re
from datetime import datetime, timezone
from typing import Tuple, Dict, Any, Optional, List
import streamlit as st
from dotenv import load_dotenv

from ai_engine import TacticalAIEngine, TacticalStrategyResult
from report_generator import generate_mission_dossier

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="T.A.R.A - AI Tactical Strategy Agent | Tactical AI Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pre-defined Tactical Sample Scenarios for quick user testing
SAMPLE_SCENARIOS = {
    "Coastal Defense & Anti-Ship Infiltration": (
        "Red Team has deployed a dense anti-access/area-denial (A2/AD) network along the eastern coastline "
        "consisting of long-range coastal radars and S-400 SAM batteries. Blue Team strike force must infiltrate "
        "via a narrow maritime basin, suppress Red Team air defenses, and escort amphibious landing units to OBJ CHARLIE."
    ),
    "Air Defense Suppression & Radar Jamming": (
        "Red Team airborne early warning (AEW) assets and mobile SAM launchers are actively painting friendly airspace. "
        "Blue Team requires an immediate Suppression of Enemy Air Defenses (SEAD) plan using passive ESM tracking, "
        "CSM communications warfare, and high-speed anti-radiation missiles."
    ),
    "Armored Column River Crossing & Interdiction": (
        "Red Team 3rd Armored Division is advancing towards Sector 7 with heavy mobile artillery and EW jamming support. "
        "Blue Team reconnaissance must establish MGRS rally points, designate Threat Zones, and execute a synchronized "
        "flanking interdiction using precision guided munitions."
    )
}


def update_preset_scenario_callback() -> None:
    """Callback function to synchronize preset dropdown selection into the text area."""
    selected_preset = st.session_state.get("preset_choice_widget")
    if selected_preset and selected_preset in SAMPLE_SCENARIOS:
        st.session_state["scenario_text_widget"] = SAMPLE_SCENARIOS[selected_preset]


def validate_scenario_briefing(text: str) -> Tuple[bool, str]:
    """Validates user scenario briefing text to ensure meaningful tactical input."""
    cleaned = text.strip()
    if len(cleaned) < 15:
        return False, "Mission briefing is too short. Please enter a detailed tactical scenario (minimum 15 characters)."
    
    # Check for random gibberish / non-words
    words = cleaned.split()
    tactical_keywords = ["team", "red", "blue", "radar", "force", "mgrs", "attack", "defense", "zone", "air", "sea", "land", "unit", "enemy", "strike", "sam", "esm", "iff"]
    has_keyword = any(kw in cleaned.lower() for kw in tactical_keywords)
    
    if len(words) < 3 and not has_keyword:
        return False, "Invalid mission briefing text. Please enter a meaningful tactical scenario describing enemy forces, objectives, or operational parameters."
        
    return True, ""


def main() -> None:
    """Main application loop and Streamlit UI layout using native components."""

    # Sidebar Controls & API Configuration
    with st.sidebar:
        st.header("SIMULATOR CONTROLS")
        st.divider()
        
        default_gemini_key = os.getenv("GEMINI_API_KEY", "")
        api_key_input = st.text_input(
            "Gemini API Key",
            value="" if default_gemini_key == "your_gemini_api_key_here" else default_gemini_key,
            type="password",
            key="gemini_api_key_widget",
            help="Enter your Google Gemini API Key. If left blank, offline simulation mode is used."
        )

        provider_choice = st.selectbox(
            "AI Engine Mode",
            options=["auto", "gemini", "groq", "simulation"],
            index=0,
            key="provider_choice_widget",
            help="Select preferred LLM provider or offline simulation."
        )

        st.divider()
        st.header("WAR GAME PARAMETERS")
        
        blue_count = st.number_input(
            "Blue Team Force Count",
            min_value=1,
            max_value=1000,
            value=14,
            step=1,
            key="blue_count_widget"
        )
        red_count = st.number_input(
            "Red Team Force Count",
            min_value=1,
            max_value=2000,
            value=28,
            step=1,
            key="red_count_widget"
        )
        threat_level = st.selectbox(
            "Assessed Threat Level",
            ["Low", "Medium", "High", "CRITICAL // SEVERE"],
            index=2,
            key="threat_level_widget"
        )
        weather_cond = st.selectbox(
            "Weather / Environmental",
            ["Clear Skies / Optimal Vis", "Low Visibility / Heavy Fog", "Night Operations / Zero Illumination", "Monsoon Rain & High Winds"],
            index=1,
            key="weather_cond_widget"
        )

        st.divider()
        st.markdown(
            "**Tactical AI Terminology Specs:**\n"
            "- **Blue Team** vs **Red Team**\n"
            "- Sensors: **Radars**, **IFF**, **ESM**, **CSM**\n"
            "- Tactics: Engagement Policy, Detection Mode, Formation Type\n"
            "- Coordinates: MGRS & Threat Zones"
        )

    # Main Header
    st.title("T.A.R.A - AI TACTICAL STRATEGY AGENT")
    st.caption("TACTICAL AI DEFENSE WAR MISSION SIMULATION ENGINE | AUTOMATED MILITARY BATTLE PLANNING")

    # Quick Scenario Selector
    st.subheader("1. Select or Enter Mission Scenario")
    st.selectbox(
        "Load Preset Tactical Scenario (Optional)",
        options=["-- Custom Scenario --"] + list(SAMPLE_SCENARIOS.keys()),
        index=0,
        key="preset_choice_widget",
        on_change=update_preset_scenario_callback
    )

    scenario_text = st.text_area(
        "Mission Scenario Briefing Input",
        height=140,
        key="scenario_text_widget",
        placeholder="Enter tactical situation, enemy dispositions, operational objectives, and terrain parameters..."
    )

    col_btn, _ = st.columns([1, 3])
    
    with col_btn:
        generate_clicked = st.button("GENERATE STRATEGY", use_container_width=True)

    # Action Execution
    if generate_clicked:
        is_valid, val_msg = validate_scenario_briefing(scenario_text)
        if not is_valid:
            st.warning(val_msg)
            return

        with st.spinner("Processing tactical parameters... Running Tactical AI Strategy Simulation..."):
            engine = TacticalAIEngine(api_key=api_key_input, provider=provider_choice)
            
            result: TacticalStrategyResult = engine.generate_strategy(
                scenario_text=scenario_text,
                blue_team_count=blue_count,
                red_team_count=red_count,
                threat_level=threat_level,
                weather_conditions=weather_cond
            )

            st.session_state["tactical_result"] = result
            st.session_state["scenario_text"] = scenario_text
            st.session_state["generation_timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            st.session_state["active_blue_count"] = blue_count
            st.session_state["active_red_count"] = red_count

    # Render Results if available in Session State
    if "tactical_result" in st.session_state:
        result: TacticalStrategyResult = st.session_state["tactical_result"]
        scenario_input_text = st.session_state["scenario_text"]
        ts_str = st.session_state["generation_timestamp"]
        active_blue = st.session_state.get("active_blue_count", blue_count)
        active_red = st.session_state.get("active_red_count", red_count)

        st.divider()
        st.header("TACTICAL AI MISSION TACTICAL ANALYSIS & BLUEPRINT")

        # Surfacing Error Diagnostics if API failed or fell back to Offline Mode
        if "Offline" in result.provider_used:
            st.info("Engine Telemetry Notice: Running under Tactical AI Offline Rule Engine.")
            if result.error_details:
                with st.expander("View API Error Diagnostics & Failure Log", expanded=True):
                    st.error(f"Diagnostic Error Trace:\n```text\n{result.error_details}\n```")

        # Top Metric Banner using synchronized session state parameters
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        # Calculate numeric percentage for progress bar and force ratio
        try:
            prob_num = int(re.sub(r"[^\d]", "", result.success_probability))
        except Exception:
            prob_num = 85
            
        force_ratio = round(active_blue / max(active_red, 1), 1)
        
        # Concise AI Model Display Name to prevent truncation
        raw_prov = result.provider_used.lower()
        if "gemini-2.0" in raw_prov:
            clean_model_name = "Gemini 2.0 Flash"
        elif "gemini-1.5-pro" in raw_prov:
            clean_model_name = "Gemini 1.5 Pro"
        elif "gemini-1.5-flash" in raw_prov:
            clean_model_name = "Gemini 1.5 Flash"
        elif "gemini" in raw_prov:
            clean_model_name = "Google Gemini"
        elif "llama-3.3" in raw_prov:
            clean_model_name = "Groq Llama-3.3"
        elif "groq" in raw_prov:
            clean_model_name = "Groq AI"
        elif "offline" in raw_prov or "rule" in raw_prov:
            clean_model_name = "Tactical AI Rule Engine"
        else:
            clean_model_name = result.provider_used.split()[0]

        # Clean threat string to fit card
        clean_threat = threat_level.split(" //")[0].strip()

        with m_col1:
            st.metric(
                label="Winning Chance",
                value=result.success_probability,
                delta="High Probability" if prob_num >= 75 else ("Moderate" if prob_num >= 50 else "High Risk"),
                delta_color="normal" if prob_num >= 75 else "inverse"
            )
        with m_col2:
            is_blue_leading = active_blue >= active_red
            ratio_delta = f"{force_ratio}:1 Blue Lead" if is_blue_leading else f"1:{round(active_red / max(active_blue, 1), 1)} Red Lead"
            st.metric(
                label="Force Balance",
                value=f"{active_blue} vs {active_red}",
                delta=ratio_delta,
                delta_color="normal" if is_blue_leading else "inverse"
            )
        with m_col3:
            is_high_threat = "CRITICAL" in threat_level.upper() or "HIGH" in threat_level.upper()
            st.metric(
                label="Threat Level",
                value=clean_threat,
                delta="Severe Risk" if is_high_threat else "Standard Risk",
                delta_color="inverse" if is_high_threat else "normal"
            )
        with m_col4:
            st.metric(
                label="AI Model",
                value=clean_model_name,
                delta="Active Strategy Engine",
                delta_color="off"
            )

        # Winning Chance Status & Visual Progress Bar
        st.write(f"**Mission Victory Prognosis:** **{prob_num}% Chance of Mission Winning / Success**")
        st.progress(min(max(prob_num / 100.0, 0.0), 1.0))
        st.divider()

        st.subheader("VISIBLE STRATEGY EXECUTION SECTIONS")

        # SECTION 1 - Native Streamlit Box
        st.subheader("SECTION 1 - PRIMARY ENGAGEMENT STRATEGY")
        st.info(result.primary_strategy)

        # SECTION 2 - Native Streamlit Box
        st.subheader("SECTION 2 - RESOURCES REQUIRED (SENSORS: RADARS, IFF, ESM, CSM)")
        st.warning(result.resources_required)

        # SECTION 3 - Native Streamlit Box
        st.subheader("SECTION 3 - ROUTES TO EXECUTE (MGRS & THREAT ZONES)")
        st.success(result.routes_to_execute)

        # SECTION 4 - MANDATORY EXPANDER RULE
        st.subheader("ALTERNATIVE & CONTINGENCY STRATEGIES")
        with st.expander("Explore Alternative Strategies", expanded=False):
            st.write(result.alternative_strategies)

        # AUTOMATED REPORT GENERATION & DOWNLOAD BUTTON
        st.divider()
        st.subheader("MISSION DOSSIER GENERATION")
        
        parsed_dict = {
            "section_1": result.primary_strategy,
            "section_2": result.resources_required,
            "section_3": result.routes_to_execute,
            "section_4": result.alternative_strategies
        }
        
        dossier_text = generate_mission_dossier(
            scenario_input=scenario_input_text,
            raw_ai_output=result.raw_response,
            parsed_sections=parsed_dict,
            provider_used=result.provider_used,
            timestamp=ts_str
        )

        st.download_button(
            label="DOWNLOAD MISSION DOSSIER (.MD)",
            data=dossier_text,
            file_name=f"MISSION_DOSSIER_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
