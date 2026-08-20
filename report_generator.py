"""
report_generator.py

Automated Military Dossier & Report Generator for Tactical AI Mission Simulator.
Formats tactical scenarios, AI strategies, operational assets, and alternative plans
into a standardized, classified downloadable military report (Markdown / Text format).

Author: Lead AI Engineer
Version: 2.1.0
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional


def generate_mission_dossier(
    scenario_input: str,
    raw_ai_output: str,
    parsed_sections: Optional[Dict[str, str]] = None,
    provider_used: str = "Tactical AI Engine",
    classification_level: str = "CLASSIFIED // TACTICAL SIMULATION ONLY",
    timestamp: Optional[str] = None
) -> str:
    """
    Formats the user's mission input and AI tactical output into a classified military dossier.

    Args:
        scenario_input: User-entered tactical scenario text.
        raw_ai_output: Complete LLM generated response.
        parsed_sections: Optional dictionary of parsed strategy sections.
        provider_used: Name of the AI provider or engine used.
        classification_level: Security classification banner text.
        timestamp: Optional ISO formatted timestamp string.

    Returns:
        A beautifully formatted Markdown string representing the complete mission dossier.
    """
    utc_now = datetime.now(timezone.utc)
    current_time = timestamp or utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
    parsed = parsed_sections or {}

    dossier_content = f"""================================================================================
{classification_level}
TACTICAL AI DEFENSE WAR MISSION SIMULATION - TACTICAL STRATEGY DOSSIER
================================================================================

DOCUMENT CONTROL NUMBER: DOSSIER-TARA-{utc_now.strftime('%Y%m%d-%H%M%S')}
GENERATION TIMESTAMP:   {current_time}
AI STRATEGY ENGINE:     {provider_used}
SECURITY CLASSIFICATION: {classification_level}

--------------------------------------------------------------------------------
0. MISSION SCENARIO OVERVIEW & INPUT DATA
--------------------------------------------------------------------------------
[SCENARIO BRIEFING]
{scenario_input.strip()}

--------------------------------------------------------------------------------
SECTION 1 - PRIMARY ENGAGEMENT STRATEGY (BLUE TEAM VS RED TEAM)
--------------------------------------------------------------------------------
{parsed.get("section_1", raw_ai_output).strip()}

--------------------------------------------------------------------------------
SECTION 2 - RESOURCES REQUIRED (RADARS, IFF, ESM, CSM)
--------------------------------------------------------------------------------
{parsed.get("section_2", "Detailed in main strategy body.").strip()}

--------------------------------------------------------------------------------
SECTION 3 - ROUTES TO EXECUTE (MGRS COORDINATES & THREAT ZONES)
--------------------------------------------------------------------------------
{parsed.get("section_3", "Detailed in main strategy body.").strip()}

--------------------------------------------------------------------------------
SECTION 4 - ALTERNATIVE STRATEGIES & REJECTION ANALYSIS (PLAN B / PLAN C)
--------------------------------------------------------------------------------
{parsed.get("section_4", "Alternative plans section unavailable.").strip()}

================================================================================
END OF DOSSIER // {classification_level}
================================================================================
"""
    return dossier_content
