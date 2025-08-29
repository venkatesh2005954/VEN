from transformers import pipeline
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_pipeline():
    # Loads once (first call will download small model)
    return pipeline("text2text-generation", model="t5-small")


STYLE_INSTRUCTIONS = {
    "Suspenseful": "Rewrite the text in a tense, suspenseful, cinematic thriller tone. Use short beats, hints, and sensory details.",
    "Dramatic": "Rewrite the text with dramatic flair and high emotional stakes.",
    "Poetic": "Rewrite the text with lyrical, poetic language and imagery.",
    "Funny": "Rewrite the text with light humor and witty phrasing.",
}


def transform_text(text: str, style: str) -> str:
    if style == "Neutral" or not text.strip():
        return text
    pipe = _get_pipeline()
    instr = STYLE_INSTRUCTIONS.get(
        style, f"Rewrite the text in a {style.lower()} tone."
    )
    prompt = f"{instr}\n\nText:\n{text}"
    # Conservative sampling to avoid runaways; adjust to taste
    out = pipe(
        prompt,
        max_length=min(512, len(text) + 120),
        do_sample=True,
        top_k=50,
        top_p=0.92,
    )[0]["generated_text"]
    return out
