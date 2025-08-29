import os
import streamlit as st
import uuid
import asyncio
import edge_tts

# --------------------------
# Function: Convert text to speech
# --------------------------
async def text_to_speech(text, voice_choice, folder="audio_files"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"output_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(folder, filename)

    # Pick voices (Microsoft Edge TTS voices)
    voice = "en-US-GuyNeural" if voice_choice == "Male" else "en-US-JennyNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filepath)

    return filepath

# Wrapper to run async in Streamlit
def run_tts(text, voice_choice):
    return asyncio.run(text_to_speech(text, voice_choice))

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="Text to Speech", page_icon="🎙️", layout="centered")
st.title("🎙️ Text to Speech App")

# Text input area
user_text = st.text_area("Enter text here:", placeholder="Type something...")

# Dropdown for voice selection
voice_choice = st.selectbox("Choose Voice:", ["-- Select Voice --", "Male", "Female"])

# Generate audio when text & valid voice selected
if user_text.strip() != "" and voice_choice in ["Male", "Female"]:
    filepath = run_tts(user_text, voice_choice)
    with open(filepath, "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")
