import streamlit as st
from typing import List
from core.models import HistoryItem


def header():
    st.markdown(
        "<h2 style='color:#c084fc; margin:0'>🎙️ Echoverse</h2>", unsafe_allow_html=True
    )


def text_input_block():
    st.markdown("### 📄 Text Input")
    text = st.text_area(
        "Enter your text here or upload a file...",
        height=150,
        label_visibility="collapsed",
    )
    file = st.file_uploader("Upload File (.txt)", type=["txt"])
    if file:
        try:
            text = file.read().decode("utf-8")
        except Exception:
            st.warning("Could not decode file as UTF-8.")
    return text


def voice_tone_style():
    st.markdown("### 🎤 Voice")
    voice = st.selectbox("Select Voice", ["Default (Google TTS)"], index=0)

    st.markdown("### 🎚 Tone")
    tone = st.selectbox(
        "Tone Modification", ["Neutral", "Formal", "Casual", "Energetic"], index=0
    )

    st.markdown("### ✨ Style Transfer")
    style = st.selectbox(
        "Text Style", ["Neutral", "Suspenseful", "Dramatic", "Poetic", "Funny"], index=0
    )
    return voice, tone, style


def generate_button(label="🎧 Generate Audio"):
    return st.container().button(label, type="primary", use_container_width=True)


def history_panel(items: List[HistoryItem]):
    st.markdown("### 📜 History")
    with st.container():
        st.markdown('<div class="ev-history">', unsafe_allow_html=True)
        if not items:
            st.info("Your audio history will appear here.")
        for i, item in enumerate(items, start=1):
            st.markdown(f"**{i}. {item.voice} | {item.tone} | {item.style}**")
            preview = (
                (item.text_input[:100] + "…")
                if len(item.text_input) > 100
                else item.text_input
            )
            st.write(preview)
            st.audio(item.audio_path)
            st.markdown("<hr />", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def clear_history_button():
    return st.button("🧹 Clear History", use_container_width=True)
