import streamlit as st
from datetime import datetime
from uuid import uuid4
from gtts import gTTS
import os

# -----------------------------
# Setup
# -----------------------------
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# -----------------------------
# History Classes
# -----------------------------
class HistoryItem:
    def __init__(self, id, text_input, text_styled, voice, tone, style, audio_path, created_at):
        self.id = id
        self.text_input = text_input
        self.text_styled = text_styled
        self.voice = voice
        self.tone = tone
        self.style = style
        self.audio_path = audio_path
        self.created_at = created_at

class HistoryRepo:
    def __init__(self):
        self.file = "history.txt"

    def load(self):
        if not os.path.exists(self.file):
            return []
        items = []
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 7:
                    id, text_input, text_styled, voice, tone, style, audio_path = parts
                    if os.path.exists(audio_path):
                        items.append(
                            HistoryItem(
                                id=id,
                                text_input=text_input,
                                text_styled=text_styled,
                                voice=voice,
                                tone=tone,
                                style=style,
                                audio_path=audio_path,
                                created_at=datetime.utcnow()
                            )
                        )
        return items

    def save_all(self, items):
        with open(self.file, "w", encoding="utf-8") as f:
            for item in items:
                f.write(
                    f"{item.id}|{item.text_input}|{item.text_styled}|{item.voice}|{item.tone}|{item.style}|{item.audio_path}\n"
                )

    def clear(self):
        if os.path.exists(self.file):
            os.remove(self.file)
            print(f"[{datetime.now()}] History file cleared.")

# -----------------------------
# Utility Functions
# -----------------------------
def transform_text(text: str, style: str) -> str:
    if style == "Formal":
        return text.capitalize() + "."
    elif style == "Casual":
        return f"Hey! {text}"
    elif style == "Funny":
        return f"{text} 😂"
    return text

def synth_to_file(text: str) -> str:
    filename = os.path.join(AUDIO_DIR, f"audio_{uuid4().hex}.mp3")
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Echoverse", layout="wide")

repo = HistoryRepo()
if "history" not in st.session_state:
    st.session_state.history = repo.load()

st.title("🎶 Echoverse - Text to Speech with Style")

left, right = st.columns([2, 1])

with left:
    text = st.text_area("📄 Enter text", height=150)
    voice = st.selectbox("🎤 Choose Voice", ["Default", "Soft", "Bold"])
    tone = st.selectbox("🎚 Choose Tone", ["Neutral", "Happy", "Sad"])
    style = st.selectbox("✨ Choose Style", ["Normal", "Formal", "Casual", "Funny"])

    if st.button("🎧 Generate Audio"):
        if not text.strip():
            st.warning("Please provide some text or upload a .txt file.")
        else:
            with st.spinner("Transforming text..."):
                styled = transform_text(text, style)

            with st.spinner("Generating speech..."):
                mp3_path = synth_to_file(styled)

            item = HistoryItem(
                id=uuid4().hex,
                text_input=text,
                text_styled=styled,
                voice=voice,
                tone=tone,
                style=style,
                audio_path=mp3_path,
                created_at=datetime.utcnow()
            )
            st.session_state.history.insert(0, item)
            repo.save_all(st.session_state.history)

            st.success("✅ Done! Playing the latest audio ↓")
            if os.path.exists(mp3_path):
                with open(mp3_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")

with right:
    st.subheader("📜 History")
    if st.session_state.history:
        for h in st.session_state.history:
            if os.path.exists(h.audio_path):
                with st.expander(f"{h.text_input[:30]}..."):
                    st.write("**Styled Text:**", h.text_styled)
                    st.write("**Voice:**", h.voice)
                    st.write("**Tone:**", h.tone)
                    st.write("**Style:**", h.style)
                    with open(h.audio_path, "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")

    if st.session_state.history and st.button("🗑 Clear History"):
        repo.clear()
        st.session_state.history = []
        st.success("History cleared.")
        st.rerun()
