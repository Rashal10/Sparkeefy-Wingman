import html
import json

import streamlit as st
import streamlit.components.v1 as components

from wingman.service import WingmanService

st.set_page_config(
    page_title="Sparkeefy AI Wingman",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

EXAMPLE_SCENARIOS = [
    {"label": "Dry haha reply", "prompt": "she replied haha after I sent a long message"},
    {"label": "Left on read", "prompt": "left on read for 2 days after a good first date"},
    {"label": "Double text regret", "prompt": "I double texted and instantly regretted it"},
    {"label": "Ask her out", "prompt": "want to ask her out without sounding desperate"},
    {"label": "She said k", "prompt": "I suggested dinner Saturday and she just replied k"},
    {"label": "Miss her LDR", "prompt": "long distance for 3 weeks and I miss her, want to say it without sounding clingy"},
]

NONE_OPTION = "Select..."
RELATIONSHIP_OPTIONS = [
    NONE_OPTION,
    "new match",
    "talking stage",
    "crush",
    "situationship",
    "dating",
    "relationship",
    "parents",
    "siblings",
    "friend",
]
EMOTION_OPTIONS = [
    NONE_OPTION,
    "anxious",
    "confused",
    "hopeful",
    "frustrated",
    "guilty",
    "overthinking",
    "calm",
    "sad",
    "guilty"
]

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stToolbar"],
    #MainMenu,
    footer { display: none !important; visibility: hidden !important; }

    .stApp {
        background:
            radial-gradient(ellipse 90% 55% at 50% -5%, rgba(255, 107, 138, 0.20), transparent 58%),
            radial-gradient(ellipse 55% 35% at 100% 20%, rgba(255, 142, 107, 0.08), transparent 50%),
            #08090d;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stMainBlockContainer"],
    .block-container {
        max-width: 920px !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: 2.75rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    section.main > div {
        max-width: 920px;
        margin: 0 auto;
    }

    .hero {
        text-align: center;
        margin: 0 auto 1.75rem auto;
        max-width: 720px;
    }
    .hero-eyebrow {
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #ff8da6;
        margin-bottom: 0.55rem;
    }
    .hero-name {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: #f4f4f5;
        margin-bottom: 0.85rem;
    }
    .hero-title {
        font-size: clamp(1.65rem, 3.2vw, 2.25rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.03em;
        margin: 0;
        color: #fafafa;
    }
    .hero-title em {
        font-style: normal;
        background: linear-gradient(135deg, #ffffff 0%, #ffb3c6 55%, #ff8e6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .wingman-shell {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 24px !important;
        padding: 2rem 2.1rem 1.75rem 2.1rem !important;
        margin: 0 auto 1.25rem auto !important;
        max-width: 920px;
        width: 100%;
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(14px);
        box-sizing: border-box;
    }
    .shell-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        color: #ff8da6;
        margin: 0 0 0.4rem 0;
    }
    .shell-hint {
        color: rgba(244, 244, 245, 0.52);
        font-size: 0.92rem;
        line-height: 1.55;
        margin: 0 0 1.35rem 0;
    }
    .shell-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.07);
        margin: 1.35rem 0 1.1rem 0;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 0.85rem;
    }
    .card-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #ff8da6;
        margin-bottom: 0.5rem;
    }
    .card-body {
        color: #f4f4f5;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
        white-space: pre-wrap;
    }

    .confidence-wrap {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        margin: 1rem 0 0.25rem 0;
    }
    .confidence-bar {
        flex: 1;
        height: 6px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #ff6b8a, #ff8e6b);
    }
    .confidence-caption {
        font-size: 0.78rem;
        font-weight: 600;
        color: rgba(244, 244, 245, 0.55);
        margin: 0.35rem 0 0.25rem 0;
    }
    .follow-up-card {
        border-color: rgba(255, 142, 107, 0.22) !important;
    }
    .results-shell {
        margin-top: 1.25rem;
    }
    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, #ff6b8a, #ff8e6b) !important;
    }

    .msg-card {
        background: rgba(21, 25, 34, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.65rem;
    }
    .msg-card p {
        color: #f4f4f5;
        font-size: 0.98rem;
        line-height: 1.6;
        margin: 0;
    }

    .user-bubble {
        background: rgba(255, 107, 138, 0.10);
        border: 1px solid rgba(255, 107, 138, 0.18);
        border-radius: 16px 16px 4px 16px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 1rem;
        color: #f4f4f5;
        font-size: 0.95rem;
        line-height: 1.55;
    }

    div[data-testid="stButton"] button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        transform: translateY(-1px);
    }
    div[data-testid="stButton"] button[kind="primary"] {
        width: 100%;
        padding: 0.9rem 1.2rem !important;
        border: none !important;
        background: linear-gradient(135deg, #ff6b8a 0%, #ff8e6b 100%) !important;
        box-shadow: 0 8px 28px rgba(255, 107, 138, 0.32) !important;
        color: #fff !important;
        font-size: 1.02rem !important;
    }
    div[data-testid="stButton"] button[kind="secondary"] {
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: rgba(255, 255, 255, 0.04) !important;
        color: rgba(244, 244, 245, 0.88) !important;
        font-size: 0.84rem !important;
        padding: 0.5rem 0.65rem !important;
        min-height: 2.6rem !important;
    }
    div[data-testid="stButton"] button[kind="secondary"]:hover {
        border-color: rgba(255, 107, 138, 0.35) !important;
        background: rgba(255, 107, 138, 0.08) !important;
    }

    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: rgba(0, 0, 0, 0.22) !important;
        font-size: 1rem !important;
        min-height: 150px !important;
    }
    .stTextArea textarea:focus {
        border-color: rgba(255, 107, 138, 0.45) !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 138, 0.12) !important;
    }

    div[data-testid="stSelectbox"] > div > div {
        border-radius: 12px !important;
        background: rgba(0, 0, 0, 0.18) !important;
    }

    [data-testid="column"] {
        width: 100% !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stTextArea"]) {
        background: rgba(255, 255, 255, 0.035) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 24px !important;
        padding: 2rem 2.1rem 1.75rem 2.1rem !important;
        box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35) !important;
        backdrop-filter: blur(14px);
        margin: 0 auto !important;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stTextArea"]) > div {
        gap: 0.65rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def get_service() -> WingmanService:
    return WingmanService()


def _optional_choice(value: str) -> str | None:
    return None if value == NONE_OPTION else value


def _esc(text: str) -> str:
    return html.escape(text)


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-eyebrow">Every story starts with a spark</div>
            <div class="hero-name">Sparkeefy Wingman</div>
            <div class="hero-title">Find the <em>right words</em><br>without overthinking</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_confidence(confidence: float) -> None:
    pct = max(0, min(100, int(confidence * 100)))
    st.markdown(
        f'<p class="confidence-caption">Confidence {pct}%</p>',
        unsafe_allow_html=True,
    )
    st.progress(confidence)


def _message_card_height(message: str) -> int:
    lines = max(2, len(message) // 46 + 1)
    return min(180, max(76, 52 + lines * 22))


def render_copyable_message(index: int, message: str, result_id: int) -> None:
    st.markdown(
        f'<div class="card-label" style="margin-top:0.75rem;">Message {index}</div>',
        unsafe_allow_html=True,
    )
    card_id = f"msg_{result_id}_{index}"
    msg_json = json.dumps(message)
    escaped = _esc(message)
    height = _message_card_height(message)

    components.html(
        f"""
        <style>
            body {{
                margin: 0;
                font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif;
                background: transparent;
            }}
            .msg-copy-card {{
                position: relative;
                background: rgba(21, 25, 34, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 1rem 3rem 1rem 1.1rem;
            }}
            .msg-copy-card p {{
                color: #f4f4f5;
                font-size: 0.98rem;
                line-height: 1.6;
                margin: 0;
                white-space: pre-wrap;
                word-break: break-word;
            }}
            .copy-btn {{
                position: absolute;
                top: 0.65rem;
                right: 0.65rem;
                width: 2rem;
                height: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                color: rgba(244, 244, 245, 0.75);
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
            }}
            .copy-btn:hover {{
                background: rgba(255, 107, 138, 0.14);
                border-color: rgba(255, 107, 138, 0.35);
                color: #ffb3c6;
            }}
            .copy-btn svg {{
                width: 14px;
                height: 14px;
                fill: currentColor;
            }}
            .copy-toast {{
                position: absolute;
                top: 0.7rem;
                right: 2.75rem;
                font-size: 0.72rem;
                font-weight: 600;
                color: #ff8da6;
                opacity: 0;
                transform: translateY(2px);
                transition: opacity 0.2s ease, transform 0.2s ease;
                pointer-events: none;
            }}
            .copy-toast.show {{
                opacity: 1;
                transform: translateY(0);
            }}
        </style>
        <div class="msg-copy-card" id="{card_id}">
            <button class="copy-btn" type="button" aria-label="Copy message" title="Copy">
                <svg viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                </svg>
            </button>
            <span class="copy-toast" id="{card_id}_toast">Copied</span>
            <p>{escaped}</p>
        </div>
        <script>
            (function () {{
                const text = {msg_json};
                const btn = document.querySelector("#{card_id} .copy-btn");
                const toast = document.getElementById("{card_id}_toast");
                btn.addEventListener("click", async () => {{
                    try {{
                        await navigator.clipboard.writeText(text);
                        toast.classList.add("show");
                        setTimeout(() => toast.classList.remove("show"), 1400);
                    }} catch (err) {{
                        const area = document.createElement("textarea");
                        area.value = text;
                        document.body.appendChild(area);
                        area.select();
                        document.execCommand("copy");
                        document.body.removeChild(area);
                        toast.classList.add("show");
                        setTimeout(() => toast.classList.remove("show"), 1400);
                    }}
                }});
            }})();
        </script>
        """,
        height=height,
    )


def _render_wingman_result(result, prompt: str) -> None:
    resp = result.response

    st.markdown('<div class="card-label" style="margin-top:0.5rem;">Your situation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="user-bubble">{_esc(prompt)}</div>', unsafe_allow_html=True)

    if resp.safety_flag:
        st.warning("This situation needs a respectful boundary, not a texting tactic.")

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-label">Energy read</div>
            <p class="card-body">{_esc(resp.energy_read)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_confidence(resp.confidence)

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="card-label">Wingman says</div>
            <p class="card-body">{_esc(resp.wingman_response)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card-label">Copy ready messages</div>', unsafe_allow_html=True)
    result_id = st.session_state.get("result_id", 0)
    for i, msg in enumerate(resp.suggested_messages, 1):
        render_copyable_message(i, msg, result_id)

    if resp.follow_up_question:
        st.markdown(
            f"""
            <div class="glass-card follow-up-card">
                <div class="card-label">Optional follow up</div>
                <p class="card-body">{_esc(resp.follow_up_question)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("View raw JSON"):
        st.json(resp.to_json_dict())


def render_wingman_panel(service: WingmanService) -> None:
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "result_id" not in st.session_state:
        st.session_state.result_id = 0

    if st.session_state.pop("pending_clear", False):
        st.session_state.user_input = ""

    if "pending_input" in st.session_state:
        st.session_state.user_input = st.session_state.pop("pending_input")

    with st.container(border=True):
        st.markdown(
            """
            <div>
                <p class="shell-label">What's going on?</p>
                <p class="shell-hint">Describe the situation in your own words. Casual is fine.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        user_input = st.text_area(
            "Situation",
            height=150,
            placeholder='e.g. "she replied haha after I sent a long message"',
            label_visibility="collapsed",
            key="user_input",
        )

        st.markdown('<p class="shell-label" style="margin-top:0.25rem;">Try a scenario</p>', unsafe_allow_html=True)
        row1 = st.columns(3, gap="small")
        row2 = st.columns(3, gap="small")
        for idx, scenario in enumerate(EXAMPLE_SCENARIOS):
            col = row1[idx] if idx < 3 else row2[idx - 3]
            with col:
                if st.button(scenario["label"], key=f"ex_{idx}", type="secondary", use_container_width=True):
                    st.session_state.pending_input = scenario["prompt"]
                    st.rerun()

        st.markdown('<div class="shell-divider"></div>', unsafe_allow_html=True)

        ctx1, ctx2, ctx3 = st.columns([1, 1, 0.5], gap="medium")
        with ctx1:
            relationship_stage = st.selectbox("Relationship stage", RELATIONSHIP_OPTIONS)
        with ctx2:
            user_emotion = st.selectbox("How you're feeling", EMOTION_OPTIONS)
        with ctx3:
            st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
            if st.button("Clear", type="secondary", use_container_width=True):
                st.session_state.pop("last_prompt", None)
                st.session_state.pop("last_result", None)
                st.session_state.pending_clear = True
                st.rerun()

        go = st.button("Get Wingman Reply", type="primary", use_container_width=True)

    if go:
        if not user_input.strip():
            st.warning("Tell the Wingman what's going on first.")
            return

        with st.spinner("Finding the right words..."):
            try:
                result = service.advise(
                    user_input,
                    relationship_stage=_optional_choice(relationship_stage),
                    user_emotion=_optional_choice(user_emotion),
                )
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                return

        st.session_state.result_id = st.session_state.get("result_id", 0) + 1
        st.session_state.last_prompt = user_input.strip()
        st.session_state.last_result = result
        st.session_state.pending_clear = True
        st.rerun()

    if st.session_state.get("last_result") and st.session_state.get("last_prompt"):
        _render_wingman_result(st.session_state.last_result, st.session_state.last_prompt)


def main() -> None:
    service = get_service()
    render_hero()

    if not service.is_ready():
        st.error("Add your DeepSeek API key to `.env` before using the Wingman.")
        st.code("copy .env.example .env\n# then set DEEPSEEK_API_KEY=...", language="bash")
        st.stop()

    render_wingman_panel(service)


if __name__ == "__main__":
    main()
