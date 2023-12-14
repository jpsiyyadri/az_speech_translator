import os
import streamlit as st
import azure.cognitiveservices.speech as speechsdk

# Set up subscription key and region from environment variables
speech_key = os.environ.get("SUBSCRIPTION_KEY", "")
service_region = os.environ.get("REGION", "")

# Custom CSS to reduce font size and adjust spacing
st.markdown(
    """
    <style>
    .block-container {
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Streamlit app
st.title("Text-to-Speech Synthesizer")
st.write("Enter text and synthesize it into speech using Azure Cognitive Services.")

# User input for text
user_input = st.text_area("Enter text to synthesize", "Hello, world!")


# Function to perform speech synthesis
def speech_synthesis_to_wave_file(text):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config
    )

    # Set the voice name here
    voice = (
        "Microsoft Server Speech Text to Speech Voice (it-IT, JennyMultilingualNeural)"
    )
    speech_synthesizer.speech_synthesis_voice_name = voice

    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return file_name
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        st.error(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.error(f"Error details: {cancellation_details.error_details}")
        return None


# Synthesize button
if st.button("Synthesize"):
    with st.spinner("Synthesizing..."):
        output_file = speech_synthesis_to_wave_file(user_input)
        if output_file:
            st.success(f"Synthesis complete.")
            # Play audio option
            audio_file = open(output_file, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/wav", start_time=0)

            # Download audio option
            with open(output_file, "rb") as file:
                btn = st.download_button(
                    label="Download Audio",
                    data=file,
                    file_name=output_file,
                    mime="audio/wav",
                )
