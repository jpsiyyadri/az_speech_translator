import os
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import datetime

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

# Set up subscription key and region
speech_key = os.environ.get("SUBSCRIPTION_KEY", "")
service_region = os.environ.get("REGION", "")

# Configure speech translation
language_from = "en-US"


# Create a Streamlit app
st.title("Speech Translation App...")

# Language selection dropdown
language_options = {"French": "fr", "Italian": "it", "Hindi": "hi", "Greek": "el"}
selected_language = st.selectbox(
    "Select Language for Translation", list(language_options.keys())
)
language_to = language_options[selected_language]

# Create the translation config
translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription=speech_key,
    region=service_region,
    speech_recognition_language=language_from,
    target_languages=(language_to,),
)

# Upload audio file
uploaded_audio_file = st.file_uploader("Upload Audio File", type="wav")

# Loading indicator
loading_indicator = st.empty()

# Download button and audio player
download_button_key = "download_button"
translated_audio_key = "translated_audio"
translated_audio = st.empty()

# Create audio config
if uploaded_audio_file:
    audio_filename = uploaded_audio_file.name
    audio_bytes = uploaded_audio_file.getvalue()
    with open(audio_filename, "wb") as f:
        f.write(audio_bytes)

    audio_config = speechsdk.audio.AudioConfig(filename=audio_filename)

    # Create speech translation recognizer
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config
    )

    # Create speech config
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )

    # Create speech synthesizer and output config
    translated_audio_filename = "translated.wav"
    op_audio_config = speechsdk.audio.AudioOutputConfig(
        filename=translated_audio_filename
    )
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=op_audio_config
    )

    # Start translation
    try:
        while True:
            # Recognize speech
            result = recognizer.recognize_once_async().get()

            # Check translation result
            if result.reason == speechsdk.ResultReason.TranslatedSpeech:
                # Display result in a box
                st.json(
                    result.json
                )  # Changed from st.write to st.json for better formatting

                # Translate and synthesize text
                translated_text = result.translations[language_to]

                try:
                    # Attempt to synthesize text
                    synth_res = synthesizer.speak_text_async(translated_text).get()

                    # Check result
                    if (
                        synth_res.reason
                        == speechsdk.ResultReason.SynthesizingAudioCompleted
                    ):
                        print("Speech synthesis completed")

                        # Show audio player
                        translated_audio.audio(
                            translated_audio_filename, format="audio/wav", start_time=0
                        )

                    elif synth_res.reason == speechsdk.ResultReason.Canceled:
                        cancellation = synth_res.cancellation_details
                        if (
                            cancellation.reason
                            != speechsdk.CancellationReason.EndOfStream
                        ):
                            print(f"Speech synthesis canceled: {cancellation.reason}")
                            if (
                                cancellation.reason
                                == speechsdk.CancellationReason.Error
                            ):
                                if cancellation.error_details:
                                    print(
                                        f"Error details: {cancellation.error_details}"
                                    )
                            print(f"Canceled text: {translated_text}")
                except Exception as synth_error:
                    print(f"Error during speech synthesis: {synth_error}")
                    break  # Terminate the loop in case of synthesis error

            else:
                # Handle other result reasons
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    print(f"Recognized: '{result.text}'")
                elif result.reason == speechsdk.ResultReason.NoMatch:
                    print("Error: No speech could be recognized")
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    if (
                        cancellation_details.reason
                        != speechsdk.CancellationReason.EndOfStream
                    ):
                        print(
                            f"Error: Speech recognition canceled. Reason: {cancellation_details.reason}"
                        )

                # Terminate the loop
                break

    except Exception as e:
        st.error(f"Error: {e}")
