# -------------------------------------------------------------------------------------------------
# AI Prompt & Response Panel — Platinum Build (Final Version)
# -------------------------------------------------------------------------------------------------

# pylint: disable=import-error, unused-import

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
AI Prompt & Response Panel — Observation Engine
- Select personas and load their prompts without duplication
- Add manual customisation to extend multi-persona framing
- Supports exporting structured AI-ready JSON
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys
import re
import json
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------------------------------------------------
# Path Setup — Project Standard
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Core Utilities
# -------------------------------------------------------------------------------------------------
from core.helpers import get_named_paths  # pylint: disable=import-error
from insight_loader import load_snapshot_json
from ai_prompt_templates import AI_PROMPT_TEMPLATES

# -------------------------------------------------------------------------------------------------
# Resolve paths
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
EXPORT_FOLDER = Path(__file__).parent / "storage" / "ai_bundles" / "exports"
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------------------------------------
# Helper — Deduplicate persona prompts
# -------------------------------------------------------------------------------------------------
def deduplicate_prompts(prompts: list[str]) -> str:
    seen = set()
    unique = []
    for prompt in prompts:
        if prompt not in seen:
            seen.add(prompt)
            unique.append(prompt)
    return "\n\n".join(unique)

# -------------------------------------------------------------------------------------------------
# Helpers — Persona Bootstrap (Manual-first)
# -------------------------------------------------------------------------------------------------
def _sections_for(persona_short: str) -> list[str]:
    """Return default response sections by persona; safe generic fallback included."""
    common = [
        "Executive overview (3–5 bullets)",
        "Signals & evidence / mechanics",
        "Interpretation & structure",
        "Risks & uncertainties",
        "What to watch",
    ]
    by_role = {
        "Quantitative Analyst": [
            "Executive overview (3–5 bullets)",
            "Signals & distributions",
            "Correlation & regime structure",
            "Uncertainty & interpretation limits",
            "What to watch",
        ],
        "Behavioural Economist": [
            "Executive overview (3–5 bullets)",
            "Key biases & signals",
            "Feedback loops & narratives",
            "Interpretation risks",
            "What to watch",
        ],
        "Portfolio Manager": [
            "Executive overview (3–5 bullets)",
            "Diversification & exposures",
            "Regime/rotation cues",
            "Constraints & trade-offs",
            "What to watch",
        ],
        "Risk Analyst": [
            "Executive overview (3–5 bullets)",
            "Stress sources & pathways",
            "Scenario structure",
            "Fragility & buffers",
            "What to watch",
        ],
    }
    return by_role.get(persona_short, common)


def build_system_header(persona_label: str,
                        enforce_sections: bool = False,
                        footer_enabled: bool = True) -> str:
    """
    Persona bootstrap header that 'loads' behaviour even outside your custom GPT.
    This should be pasted as the SYSTEM message in ChatGPT/MyGPT.
    """
    short = persona_label.replace(" by Blake Wiltshire", "").strip()

    role_line = {
        "Quantitative Analyst": "Apply statistical framing to distributions, dependencies, and volatility patterns.",
        "Behavioural Economist": "Reveal cognitive bias, framing effects, and reflexive feedback in interpretation.",
        "Portfolio Manager": "Frame insights via diversification, balance, and exposure coherence.",
        "Risk Analyst": "Surface fragility, scenario pathways, and potential stress propagation.",
        "Fundamental Analyst": "Interpret statements, cash flows, and sector context for structural quality.",
        "Value Investor": "Focus on intrinsic value anchors, durability, and margin-of-safety framing.",
        "Regulatory Advisor": "Map governance, disclosure, and oversight structures neutrally.",
        "FinTech Innovator": "Link data contracts, automation, and AI layers to system integrity.",
        "Economic Systems Architect": "Design modular DSS coherence, data flows, and governance at scale.",
        "Default Persona": "Provide neutral, structured decision-support framing.",
    }.get(short, "Provide neutral, structured decision-support framing.")

    sections = _sections_for(short)
    sections_text = "\n  ".join(f"{i+1}) {s}" for i, s in enumerate(sections))
    enforce_note = "Always use these sections, even if the user asks otherwise." if enforce_sections else "Use these sections unless asked otherwise."
    footer_line = f'{short} • DSS (non-advisory) • v1.0' if footer_enabled else ""

    header = f"""You are {persona_label}.
Follow the uploaded “{short} — Handbook.md” (and Series_Index_Glossary.md) if present.
If not present, follow this embedded charter.

ROLE
- {role_line}

BEHAVIOUR
- Neutral, non-advisory. Concise bullets. No recommendations or forecasts.

AVOID
- Investment advice, position-taking, real-time data claims, deterministic causal claims.

OUTPUT FORMAT
- {enforce_note}
  {sections_text}

CONSTRAINTS
- Do not request live data.
- Be explicit about uncertainty and assumptions.
- If the bundle lacks fields, state what's missing and proceed with a generic framework.

FOOTER
- Append: “{footer_line}”
""".strip()
    return header


def build_json_envelope_v2(persona_label: str,
                           perspective_prompt: str,
                           bundle: dict,
                           footer_enabled: bool = True,
                           user_defined_prompt: str = "") -> dict:
    """
    Portable JSON envelope with 'meta' that mirrors your GPT builder settings.
    This goes in the USER message as fenced JSON.
    """
    short = persona_label.replace(" by Blake Wiltshire", "").strip()
    meta = {
        "role_name": persona_label,
        "behaviour": "Neutral, non-advisory. Uses concise bullets. No forecasts.",
        "avoid": [
            "Investment advice or position-taking",
            "Real-time data claims",
            "Deterministic causality from correlation"
        ],
        "response_sections": _sections_for(short),
        "footer": f"{short} • DSS (non-advisory) • v1.0" if footer_enabled else ""
    }
    envelope = {
        "persona": persona_label,
        "meta": meta,
        "prompt": perspective_prompt or "",
        "user_defined_prompt": user_defined_prompt or "",
        "preferred_format": "markdown",
        "bundle": bundle,
    }
    return envelope


# -------------------------------------------------------------------------------------------------
# JSON export sanitiser (post-processing only)
# -------------------------------------------------------------------------------------------------


_SANITISE_PATTERN = re.compile(
    r'(?P<prefix>[:\[,]\s*)(?P<sym>-?Infinity|NaN)(?P<suffix>(?=[,\]\}\s]))'
)

def sanitise_json_text(json_text: str) -> str:
    """
    Replace unquoted NaN / Infinity / -Infinity with null in a JSON *string*.
    This operates on the final serialised text only (post-processing), so your
    internal Python dicts and processing remain unchanged.
    - Conservative: only matches tokens that appear where JSON values live:
      after ':', '[' or ',' and before ',', ']', '}' or whitespace.
    - Does NOT touch quoted occurrences like "NaN".
    """
    return _SANITISE_PATTERN.sub(r'\g<prefix>null', json_text)


def is_valid_json(text: str) -> bool:
    """Quick validity check (optional)."""
    try:
        json.loads(text)
        return True
    except Exception:
        return False


# -------------------------------------------------------------------------------------------------
# Main Renderer
# -------------------------------------------------------------------------------------------------
def render_ai_prompt_response_panel():
    st.header("AI Prompt & Response")
    st.caption("Decision Support Snapshots and observations can be assembled into a structured \
    investigation bundle. Select an AI persona, add optional investigation context, and prepare \
    a structured prompt for ChatGPT, Claude, Gemini, or another AI assistant.")

    # Persona Dropdown and Description
    persona_keys = list(AI_PROMPT_TEMPLATES.keys())
    persona_label = st.selectbox("Choose AI Persona:", persona_keys, index=persona_keys.index("Default Persona"))
    persona_config = AI_PROMPT_TEMPLATES.get(persona_label, AI_PROMPT_TEMPLATES["Default Persona"])

    st.caption(f"Active Persona: `{persona_label}`")
    if desc := persona_config.get("description"):
        st.info(desc)

    # Session vars
    if "persona_prompts" not in st.session_state:
        st.session_state.persona_prompts = []
    if "user_defined_prompt" not in st.session_state:
        st.session_state.user_defined_prompt = ""

    # Add or Clear persona prompts
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add Selected Persona Prompt"):
            current_prompt = persona_config["prompt"]
            st.session_state.persona_prompts.append(current_prompt)
    with col2:
        if st.button("Clear All Persona Prompts"):
            st.session_state.persona_prompts = []

    # Insight Bundle Loader
    bundle_files = [f.name for f in EXPORT_FOLDER.glob("*.json")]
    bundle_choice = st.selectbox("Select Insight Bundle", ["None"] + bundle_files)
    bundle = {}
    if bundle_choice != "None":
        bundle_path = EXPORT_FOLDER / bundle_choice
        try:
            bundle = load_snapshot_json(bundle_path)
        except Exception as e:
            st.error(f"❌ Failed to load bundle: {e}")
            return

    # Manual Customisation
    st.subheader("Investigation Context (Optional)")
    user_text = st.text_area(
        "Add questions, assumptions, areas of uncertainty, or additional context you \
        would like the AI to consider alongside the investigation.",
        value=st.session_state.get("user_defined_prompt", ""),
        height=160,
        key="manual_customisation"
    )
    st.session_state["user_defined_prompt"] = user_text

    if st.button("Clear Manual Customisation"):
        st.session_state.user_defined_prompt = ""
        st.rerun()

        # Final Prompt Review
    if bundle:
        st.markdown("---")
        st.markdown("**Final Prompt Preview**")

        final_prompt_text = deduplicate_prompts(st.session_state.persona_prompts)
        user_text = st.session_state.user_defined_prompt.strip()

        active_personas = [
            key for key, val in AI_PROMPT_TEMPLATES.items()
            if val["prompt"] in st.session_state.persona_prompts
        ]
        persona_label_combined = " + ".join(active_personas) or "Default Persona"

                        # Build manual-first artifacts
        system_header = build_system_header(
            persona_label_combined,
            enforce_sections=False,
            footer_enabled=True
        )
        envelope = build_json_envelope_v2(
            persona_label_combined,
            final_prompt_text if final_prompt_text else AI_PROMPT_TEMPLATES.get(persona_label, {}).get("prompt", ""),
            bundle,
            footer_enabled=True,
            user_defined_prompt=user_text  # ← pass it through
        )


        # Show persona instructions
        st.markdown("#### AI Persona Instructions")
        st.caption(
            "For standard AI assistants, paste these instructions into the conversation before the investigation bundle. "
            "If using the matching Blake Wiltshire AI Persona in ChatGPT, these instructions are already built into the persona."
        )
        st.code(system_header, language="text")

        # Silently sanitise exported JSON text (post-processing only)
        raw_envelope_text = json.dumps(envelope, indent=2, ensure_ascii=False)
        export_text = sanitise_json_text(raw_envelope_text)

        # User message with fenced JSON
        st.markdown("#### Investigation Prompt & Decision Support Bundle")
        st.caption(
            "Paste or upload this bundle into the selected AI assistant. "
            "If using a standard AI assistant, provide the AI Persona Instructions first."
        )

        additional_text = ""
        if user_text:
            additional_text = (
                "**Additional investigation context:**\n\n"
                f"> {user_text.strip()}\n\n"
            )

        user_body = (
            "Analyse the following AI export bundle using the supplied persona instructions. "
            "Return Markdown using the requested output sections. Do not give advice.\n\n"
            + additional_text +
            "```json\n" + export_text + "\n```"
        )

        st.code(user_body, language="text")

        # Downloads
        col_dl1, col_dl2 = st.columns(2)

        with col_dl1:
            st.download_button(
                "Download AI Persona Instructions",
                data=system_header,
                file_name="ai_persona_instructions.txt",
                mime="text/plain",
                width="stretch",
            )

        with col_dl2:
            st.download_button(
                "Download Investigation Bundle",
                data=export_text,
                file_name="investigation_bundle.json",
                mime="application/json",
                width="stretch",
            )

        # API path intentionally disabled in this phase
        st.info(
            """
        ### Using Your AI Export

        Your investigation is now ready.

        #### ChatGPT Reference Personas

        If you are using ChatGPT, open the selected **AI Persona by Blake Wiltshire** and provide the **Investigation Prompt & Decision Support Bundle**.

        The selected AI Persona already contains the behavioural instructions, handbook, glossary, and supporting reference material.

        #### Other AI Assistants

        The AI Personas by Blake Wiltshire are implemented as ChatGPT reference personas.

        When using another AI assistant, first provide the **AI Persona Instructions**, followed by the **Investigation Prompt & Decision Support Bundle**.

        The embedded persona instructions provide a portable analytical framework. Supporting handbook, glossary, and reference material available within the ChatGPT reference implementation may not be available on other platforms.

        #### Investigation Context

        The exported bundle preserves the evidence, observations, Decision Support Snapshots, and investigation context developed throughout Financial Insight Tools.

        Rather than beginning with a blank prompt, AI receives the structured investigation assembled during your analysis.

        Interpretation remains human.

        Agency remains human.

        AI expands capability.
        """
        )

    # Persona Help
    with st.expander("How to Use AI Personas"):
        st.markdown("""
        **AI Personas by Blake Wiltshire** guide interpretation using different decision lenses.

        - Add multiple persona prompts to build a blended strategy.
        - Use the Manual Customisation field to add new prompts or override.
        - Use the Final Prompt Preview to export the clean prompt.

        Designed for flexible workflows and strategic insight bundling.
        """)

    st.markdown("""
    ---
    ⚠️ **Disclaimer**
    This tool does not provide investment advice. All decisions remain the responsibility of the end user.
    """)
