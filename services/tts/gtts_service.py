from gtts import gTTS
from uuid import uuid4
from utils.paths import AUDIO_DIR


def synth_to_file(text: str, lang: str = "en") -> str:
    fn = AUDIO_DIR / f"audio_{uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(str(fn))
    return str(fn)
