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

# Dropdown for voice selection
available_voices = [
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyMultilingualV2Neural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, RyanMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, DavisNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AmberNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AnaNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AndrewNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AshleyNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, BrandonNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, BrianNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, ChristopherNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, CoraNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, ElizabethNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, EmmaNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, EricNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, JacobNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, JaneNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, JasonNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, MichelleNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, MonicaNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, NancyNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, RogerNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, SaraNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, SteffanNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, TonyNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AIGenerate1Neural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AIGenerate2Neural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AndrewMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AvaMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, AvaNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, BlueNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, BrianMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (en-US, EmmaMultilingualNeural)",
    "Microsoft Server Speech Text to Speech Voice (te-IN, ShrutiNeural)",
    "Microsoft Server Speech Text to Speech Voice (te-IN, MohanNeural)",
]

voice_selection = st.selectbox("Choose a voice", available_voices)


# Function to perform speech synthesis
def speech_synthesis_to_wave_file(text, voice):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = voice

    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config
    )

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
        output_file = speech_synthesis_to_wave_file(user_input, voice_selection)
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
