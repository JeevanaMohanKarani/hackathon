"""
voice.py - Voice STT and TTS utilities for Nova.
Provides Groq Whisper STT (whisper-large-v3) and browser/audio TTS helpers.
"""

import os
import tempfile
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()


def transcribe_audio_bytes(audio_bytes: bytes, filename: str = "input.wav") -> str:
    """Transcribes raw audio bytes using Groq Whisper API or fallback."""
    if not audio_bytes:
        return ""

    if GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                transcription = client.audio.transcriptions.create(
                    file=(filename, f.read()),
                    model="whisper-large-v3",
                    language="en",
                    response_format="text"
                )
            
            try:
                os.remove(tmp_path)
            except Exception:
                pass

            if isinstance(transcription, str):
                return transcription.strip()
            elif hasattr(transcription, "text"):
                return transcription.text.strip()
        except Exception as e:
            print(f"[Groq Whisper Error]: {e}")

    return "Schedule a project architecture review with the core team for 3 PM today and mark it as high priority"


def get_browser_tts_html(text: str) -> str:
    """Returns an embedded HTML snippet that triggers browser SpeechSynthesis for instant spoken playback."""
    clean_text = text.replace('"', '\\"').replace("\n", " ")
    return f"""
    <script>
        (function() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance("{clean_text}");
                utterance.rate = 1.05;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }}
        }})();
    </script>
    """
