"""
ai_engine.py

AI Tactical Strategy Engine for Defense War Mission Simulator (Tactical AI Framework).
Handles LLM API integration (Google Gemini / Groq Llama-3.3), system prompting,
strict Tactical AI terminology enforcement, structured response parsing with Markdown formatting,
SDK & REST fallback layers, detailed error surfacing, and offline tactical simulation.

Author: Lead AI Engineer
Version: 2.3.1
"""

import os
import re
import logging
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv

# Configure module logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


@dataclass
class TacticalStrategyResult:
    """Dataclass holding structured tactical output sections and diagnostic telemetry."""
    raw_response: str
    primary_strategy: str
    resources_required: str
    routes_to_execute: str
    alternative_strategies: str
    success_probability: str
    risk_factors: str
    provider_used: str
    error_details: Optional[str] = None


class TacticalAIEngine:
    """Core AI Tactical Engine powering the Tactical AI Mission Simulator strategy generation."""

    SYSTEM_PROMPT: str = """
You are a Chief AI Tactical Strategy Officer for the Defense War Mission Simulator (Tactical AI Framework).
Your role is to analyze battlefield scenarios and formulate coherent, mission-critical strategies with tactical depth.

═══════════════════════════════════════════════════════════════════

## CORE TERMINOLOGY & SIMULATOR FRAMEWORK

**TEAM DESIGNATION:**
- Blue Team = Friendly/Allied Forces
- Red Team = Opposing/Hostile Forces

**OPERATIONAL MAPPING:**
- All movement routes MUST use MGRS coordinates (format: ##X YY ##### #####)
- Example: "31U DQ 48215 19432" with elevation in meters
- Clearly identify "Threat Zones" with coordinate boundaries and threat radius

**SENSOR & ELECTRONIC WARFARE SYSTEMS:**
You MUST allocate these 4 critical systems and explain their roles:
1. **Radars** — Detection, tracking, fire-control systems (Active/Passive/Hybrid modes)
2. **IFF** — Identification Friend or Foe interrogator/transponder configurations
3. **ESM** — Electronic Support Measures for passive RF threat detection
4. **CSM** — Communications Support Measures for COMINT & Direction Finding

**TACTICAL PARAMETERS (Mandatory to Specify):**
- **Engagement Policy:** [Weapons Free | Weapons Tight | Hold Fire | Weapons Ready]
- **Detection Mode:** [Active Emissions | Passive Stealth | Intermittent Pulse | Hybrid]
- **Formation Type:** [Wedge | Echelon Right/Left | Spread Line | Diamond | Tactical Spread]

═══════════════════════════════════════════════════════════════════

## OUTPUT STRUCTURE (4 MANDATORY SECTIONS)

Respond with EXACTLY these 4 sections. Use markdown bullets and bold for clarity.
Each section builds on the previous one with increasing tactical detail.

### SECTION 1: PRIMARY STRATEGY & OPERATIONAL PLAN
Provide your PRIMARY recommended strategy (highest success probability).
- **Operational Approach:** [Concise tactical description of Blue Team vs Red Team engagement]
- **Rationale:** [Why this approach is optimal given the scenario]
- **Formation Type:** [Specific formation for Blue Team units]
- **Detection Mode:** [Sensor posture - Active/Passive/Hybrid]
- **Engagement Policy:** [When weapons can/should be deployed]
- **Success Probability:** [X% based on threat level and tactical factors]
- **Critical Risk Factors:**
  1. [Specific vulnerability or failure point #1]
  2. [Specific vulnerability or failure point #2]
  3. [Specific vulnerability or failure point #3 if applicable]

### SECTION 2: REQUIRED RESOURCES & ASSET ALLOCATION
Specify exact systems, quantities, and configurations for this strategy.
- **Blue Team Assets:** [Aircraft types and quantity | Ground units | Naval assets]
- **Radar Systems:** [Model/Type, coverage range, mode allocation]
- **IFF Configuration:** [Mode assignment, interrogation frequency, transponder settings]
- **ESM Suite:** [Threat detection capabilities, frequency range, integration]
- **CSM Suite:** [COMINT capabilities, DF accuracy, relay network]
- **Weapons Payload:** [Specific munitions types, quantities, targeting logic]
- **Support Systems:** [Refueling, electronic warfare, communications relay stations]

### SECTION 3: OPERATIONAL ROUTES & SPATIAL PLANNING
Define the complete operational route with terrain-aware MGRS coordinates.
- **Insertion Point:** [MGRS Coordinates | Terrain type | Elevation | Entry vector]
- **Waypoint Sequence:** [Numbered waypoints with MGRS, altitude bands, time estimates]
- **Target Engagement Zone:** [MGRS coordinates | Predicted Red Team disposition | Safe corridor for extraction]
- **Extraction Point:** [MGRS | Alternate extraction points if primary is compromised]
- **Threat Zones Avoidance:** [Red Team defensive positions with MGRS | Detection radii | Recommended buffer zones]
- **Route Rationale:** [Why this routing minimizes detection risk and maximizes operational surprise]

### SECTION 4: ALTERNATIVE STRATEGIES & CONTINGENCIES
Provide 1-2 alternative approaches with lower success probability. Explain why Primary Strategy is superior.
- **STRATEGY B - [Descriptive Name]:**
  - **Approach:** [Brief alternative tactical approach]
  - **Formation Type:** [Alternative formation]
  - **Detection Mode:** [Alternative detection posture]
  - **Success Probability:** [X%]
  - **Why Rejected:** [Specific reason this is suboptimal compared to Primary]

- **STRATEGY C - [Emergency Contingency]:** (only if scenario complexity warrants)
  - **Approach:** [Last-resort tactical approach]
  - **Formation Type:** [Contingency formation]
  - **Detection Mode:** [Detection mode for contingency]
  - **Success Probability:** [X%]
  - **When Activated:** [Specific trigger conditions for contingency activation]

═══════════════════════════════════════════════════════════════════

## QUALITY ASSURANCE CHECKLIST

Before finalizing your response, validate:
✓ All tactical parameters (Formation, Detection Mode, Engagement Policy) are explicitly stated
✓ All 4 sensor systems (Radar, IFF, ESM, CSM) are allocated with specific details
✓ MGRS coordinates follow proper formatting with elevation data
✓ Threat Zones are defined with coordinate boundaries and threat radii
✓ Risk factors are specific and actionable, not generic
✓ Success probability is calibrated to stated threat level (0-100%)
✓ Sections logically flow from strategy → resources → routes → contingencies
✓ Alternative strategies are genuinely inferior with clear rejection reasoning

═══════════════════════════════════════════════════════════════════

## TONE & COMMUNICATION STYLE

- Be **tactical and precise**: Use military terminology correctly but explain complex concepts
- Be **analytical not prescriptive**: Show reasoning for every decision
- Be **scenario-aware**: Adapt intensity and detail to scenario complexity
- Be **simulator-focused**: Remember outputs feed into Tactical AI Framework mission planning
- Be **honest about uncertainty**: Flag assumptions and data limitations
"""

    def __init__(self, api_key: Optional[str] = None, provider: str = "auto") -> None:
        """
        Initialize the AI Engine with optional explicit API key and provider choice.

        Args:
            api_key: Optional API key override. If None, loaded from env.
            provider: 'auto', 'gemini', 'groq', or 'simulation'.
        """
        env_gemini = os.getenv("GEMINI_API_KEY", "")
        # Resolve key precedence: explicit api_key -> env GEMINI_API_KEY -> None
        raw_key = api_key if api_key is not None else env_gemini
        self.api_key = raw_key if raw_key and raw_key != "your_gemini_api_key_here" else None
        
        env_groq = os.getenv("GROQ_API_KEY", "")
        self.groq_api_key = env_groq if env_groq and env_groq != "your_groq_api_key_here" else None
        
        self.provider = provider

    def generate_strategy(
        self,
        scenario_text: str,
        blue_team_count: int = 12,
        red_team_count: int = 24,
        threat_level: str = "High",
        weather_conditions: str = "Low Visibility / Heavy Fog"
    ) -> TacticalStrategyResult:
        """
        Generates a tactical strategy for the given mission scenario.

        Args:
            scenario_text: Tactical mission overview entered by the user.
            blue_team_count: Friendly unit count.
            red_team_count: Hostile unit count.
            threat_level: Operational threat assessment.
            weather_conditions: Environmental parameters.

        Returns:
            TacticalStrategyResult object containing raw and parsed strategy sections plus error diagnostics.
        """
        prompt = f"""
MISSION SCENARIO DETAILS:
------------------------
Scenario Description: {scenario_text}
Blue Team Asset Count: {blue_team_count} units
Red Team Asset Count: {red_team_count} units
Assessed Threat Level: {threat_level}
Environmental & Weather Conditions: {weather_conditions}

Generate the tactical war game strategy adhering strictly to all Tactical AI simulator terminology, section headers, and Markdown bullet formatting rules.
"""
        raw_output = ""
        provider_used = "Offline Tactical Simulator"
        error_logs: List[str] = []

        # 1. Attempt Gemini API if requested or in auto mode
        if (self.provider in ["auto", "gemini"]):
            if not self.api_key:
                error_logs.append("Gemini API Key: Missing or unconfigured.")
            else:
                try:
                    raw_output, model_used = self._call_gemini_api(prompt)
                    provider_used = f"Google Gemini ({model_used}) AI Engine"
                except Exception as e:
                    err_msg = f"Gemini API Exception: {str(e)}"
                    logger.error(err_msg)
                    error_logs.append(err_msg)
                    raw_output = ""

        # 2. Attempt Groq API if Gemini failed or Groq requested
        if not raw_output and (self.provider in ["auto", "groq"]):
            if not self.groq_api_key:
                error_logs.append("Groq API Key: Missing or unconfigured in .env.")
            else:
                try:
                    raw_output, model_used = self._call_groq_api(prompt)
                    provider_used = f"Groq ({model_used}) AI Engine"
                except Exception as e:
                    err_msg = f"Groq API Exception: {str(e)}"
                    logger.error(err_msg)
                    error_logs.append(err_msg)
                    raw_output = ""

        # 3. Fallback to local tactical simulation engine if live APIs failed/unconfigured
        if not raw_output:
            logger.info("Using local Tactical AI Simulation Engine (Offline mode).")
            raw_output = self._generate_simulated_tactical_output(
                scenario_text, blue_team_count, red_team_count, threat_level, weather_conditions
            )
            provider_used = "Tactical AI Rule Engine (Offline)"

        # Parse sections for UI presentation
        parsed = self.parse_tactical_sections(raw_output)

        combined_errors = "\n".join(error_logs) if error_logs else None

        return TacticalStrategyResult(
            raw_response=raw_output,
            primary_strategy=parsed.get("section_1", "Section 1 unavailable."),
            resources_required=parsed.get("section_2", "Section 2 unavailable."),
            routes_to_execute=parsed.get("section_3", "Section 3 unavailable."),
            alternative_strategies=parsed.get("section_4", "Section 4 unavailable."),
            success_probability=parsed.get("success_probability", "85%"),
            risk_factors=parsed.get("risk_factors", "Standard operational risk."),
            provider_used=provider_used,
            error_details=combined_errors
        )

    def _call_gemini_api(self, prompt: str) -> Tuple[str, str]:
        """Call Google Gemini API using SDK or direct REST API fallback across supported models."""
        models_to_try = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-flash-latest"]
        last_error = None

        # Method 1: Try new google-genai SDK across model candidates
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=self.api_key)
            config = types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT,
                temperature=0.2
            )
            for m in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=prompt,
                        config=config
                    )
                    if response and response.candidates:
                        parts = response.candidates[0].content.parts
                        text_parts = [p.text for p in parts if hasattr(p, 'text') and p.text and not getattr(p, 'thought', False)]
                        full_text = "".join(text_parts).strip() if text_parts else (response.text or "").strip()
                        if full_text:
                            return full_text, m
                except Exception as m_err:
                    last_error = m_err
        except ImportError:
            logger.debug("google-genai SDK not installed.")

        # Method 2: Try legacy google-generativeai SDK
        try:
            import google.generativeai as genai_legacy
            genai_legacy.configure(api_key=self.api_key)
            for m in models_to_try:
                try:
                    model = genai_legacy.GenerativeModel(
                        model_name=m,
                        system_instruction=self.SYSTEM_PROMPT
                    )
                    response = model.generate_content(prompt)
                    if response and response.candidates:
                        parts = response.candidates[0].content.parts
                        text_parts = [p.text for p in parts if hasattr(p, 'text') and p.text and not getattr(p, 'thought', False)]
                        full_text = "".join(text_parts).strip() if text_parts else (response.text or "").strip()
                        if full_text:
                            return full_text, m
                except Exception as m_err:
                    last_error = m_err
        except ImportError:
            logger.debug("google.generativeai SDK not installed.")

        # Method 3: Direct REST API Fallback (No external google SDK required)
        import requests
        for m in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={self.api_key}"
            payload = {
                "system_instruction": {
                    "parts": [{"text": self.SYSTEM_PROMPT}]
                },
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.2
                }
            }
            try:
                resp = requests.post(url, json=payload, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        text_parts = [p.get("text", "") for p in parts if p.get("text") and not p.get("thought", False)]
                        if text_parts:
                            return "".join(text_parts).strip(), m
                        elif parts and "text" in parts[-1]:
                            return parts[-1]["text"].strip(), m
                else:
                    err_json = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                    err_msg = err_json.get("error", {}).get("message", f"HTTP {resp.status_code}: {resp.text[:200]}")
                    last_error = RuntimeError(f"Model '{m}' failed -> {err_msg}")
            except Exception as req_err:
                last_error = req_err

        if last_error:
            raise last_error
        raise RuntimeError("Gemini API invocation failed on all fallback models.")

    def _call_groq_api(self, prompt: str) -> Tuple[str, str]:
        """Call Groq REST API using active supported model families (Llama-3.3-70b / Llama-3.1-8b)."""
        import requests
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        last_error = None

        for model_name in models_to_try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                if response.status_code == 200:
                    content = response.json()["choices"][0]["message"]["content"]
                    cleaned_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                    return cleaned_content, model_name
                else:
                    err_json = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
                    err_msg = err_json.get("error", {}).get("message", f"HTTP {response.status_code}: {response.text[:200]}")
                    last_error = RuntimeError(f"Groq model '{model_name}' failed -> {err_msg}")
            except Exception as e:
                logger.warning(f"Groq API call with model '{model_name}' failed: {str(e)}")
                last_error = e

        if last_error:
            raise last_error
        raise RuntimeError("All Groq API models failed.")

    def _generate_simulated_tactical_output(
        self,
        scenario: str,
        blue_count: int,
        red_count: int,
        threat: str,
        weather: str
    ) -> str:
        """Generates realistic Tactical AI-compliant tactical output formatted with Markdown bullets when offline."""
        return f"""
### SECTION 1: PRIMARY STRATEGY & OPERATIONAL PLAN
- **Operational Approach:** Blue Team will execute a coordinated low-altitude stealth penetration against Red Team assets.
- **Rationale:** Low-altitude ingress utilizing terrain masking minimizes Red Team long-range radar warning time.
- **Formation Type:** Tactical Diamond Echelon (Staggered 500m interval for optimal ESM sensor coverage).
- **Engagement Policy:** Weapons Tight until Red Team radar locks onto lead unit; then transition to Weapons Free within designated Engagement Zone.
- **Detection Mode:** Passive Stealth Scanning utilizing ESM and CSM passive receivers, holding active AESA Radar emissions to intermittent 2-second directional bursts.
- **Success Probability:** 89%
- **Critical Risk Factors:**
  1. Early detection by Red Team airborne early warning assets if Blue Team altitude exceeds 300ft AGL.
  2. Communications blackout in deep valleys disrupting CSM cross-link telemetry.

### SECTION 2: REQUIRED RESOURCES & ASSET ALLOCATION
- **Blue Team Assets:** {blue_count} Advanced Multi-Role Combat Aircraft & Unmanned Strike Escorts for Blue Team.
- **Radar Systems:** AESA AN/APG-81 Active Electronically Scanned Array operating in LPI (Low Probability of Intercept) Mode.
- **IFF Configuration:** Secure Mode 5 Level 2 Crypto-Interrogator / Transponder suite for positive Blue Team identification.
- **ESM Suite:** AN/ALR-94 Passive Electronic Support Measures receiver array covering 360-degree RF spectrum against Red Team emitters.
- **CSM Suite:** AN/ASQ-239 Communications Support Measures for real-time threat emitter geo-location and signals intelligence.
- **Weapons Payload:** 8x AIM-120D AMRAAM, 4x GBU-53/B StormBreaker Precision Guided Munitions, 2x AGM-88E AARGM Anti-Radiation Missiles.

### SECTION 3: OPERATIONAL ROUTES & SPATIAL PLANNING
- **Insertion Point:** MGRS 31U DQ 48215 19432 (Elevation: 150m MSL, terrain masking enabled).
- **Waypoint Sequence:** MGRS 31U DQ 51044 21890 to MGRS 31U DQ 55000 24000 (Stealth Corridor skirting SAM envelope).
- **Target Engagement Zone:** MGRS 31U DQ 58912 28450 (Execute strike package under ESM guidance).
- **Extraction Point:** MGRS 31U DQ 62410 31050 (Egress via low-altitude maritime channel to safe sector).
- **Threat Zones Avoidance:** Threat Zone Alpha: Red Team S-400 Radar Coverage (MGRS 31U DQ 53500 24000) - Radius 45km. Maintain terrain masking.

### SECTION 4: ALTERNATIVE STRATEGIES & CONTINGENCIES
- **STRATEGY B - Direct High-Altitude Supersonic Penetration:**
  - **Approach:** High-altitude direct penetration utilizing active radar jamming.
  - **Formation Type:** Spread Line (Wide Frontage).
  - **Engagement Policy:** Weapons Free from Maximum Engagement Range (MER).
  - **Detection Mode:** Active Radar Jamming & Full Power AESA Tracking.
  - **Success Probability:** 68%
  - **Why Rejected:** REJECTED because high-power active radar emissions immediately alert Red Team long-range SAM batteries.
- **STRATEGY C - Nighttime Low-Level Infiltration:**
  - **Approach:** Staggered nighttime infiltration via coastal basin.
  - **Formation Type:** Trail Column in Pairs.
  - **Engagement Policy:** Hold Fire until Command Authorization.
  - **Detection Mode:** Passive Infrared & CSM Listening Mode Only.
  - **Success Probability:** 54%
  - **Why Rejected:** REJECTED due to unfavorable weather conditions ({weather}) causing high risk of CFIT along narrow coastal corridors.
"""

    @staticmethod
    def parse_tactical_sections(raw_text: str) -> Dict[str, str]:
        """
        Parses raw LLM text into individual sections for UI rendering.

        Returns dict with keys: 'section_1', 'section_2', 'section_3', 'section_4',
        'success_probability', 'risk_factors'.
        """
        parsed = {}
        
        clean_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()
        
        sec1_match = re.search(r"(?:#+\s*|\*\*)*SECTION 1[^\n]*\n+(.*?)(?=(?:#+\s*|\*\*)*SECTION 2|\Z)", clean_text, re.DOTALL | re.IGNORECASE)
        sec2_match = re.search(r"(?:#+\s*|\*\*)*SECTION 2[^\n]*\n+(.*?)(?=(?:#+\s*|\*\*)*SECTION 3|\Z)", clean_text, re.DOTALL | re.IGNORECASE)
        sec3_match = re.search(r"(?:#+\s*|\*\*)*SECTION 3[^\n]*\n+(.*?)(?=(?:#+\s*|\*\*)*SECTION 4|\Z)", clean_text, re.DOTALL | re.IGNORECASE)
        sec4_match = re.search(r"(?:#+\s*|\*\*)*SECTION 4[^\n]*\n+(.*)", clean_text, re.DOTALL | re.IGNORECASE)

        parsed["section_1"] = sec1_match.group(1).strip() if sec1_match else clean_text
        parsed["section_2"] = sec2_match.group(1).strip() if sec2_match else "See raw strategy text."
        parsed["section_3"] = sec3_match.group(1).strip() if sec3_match else "See raw strategy text."
        parsed["section_4"] = sec4_match.group(1).strip() if sec4_match else "Alternative strategies section unavailable."

        prob_match = re.search(r"Success Probability[^\d]*([\d]+%)", parsed["section_1"], re.IGNORECASE)
        parsed["success_probability"] = prob_match.group(1) if prob_match else "88%"

        risk_match = re.search(r"(?:Critical\s+)?Risk Factors:(.*?)(?=SECTION 2|\Z|\n\n[A-Z])", parsed["section_1"], re.DOTALL | re.IGNORECASE)
        parsed["risk_factors"] = risk_match.group(1).strip() if risk_match else "Elevated SAM envelope risk."

        return parsed
