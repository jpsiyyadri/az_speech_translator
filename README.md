# az_speech_translator

It's a streamlit app which uses Azure Speech Service to translate the speech into a selected languages

## Prerequisite

    - Docker
    - Python
    - Azure Services

## How to run on your machine

Step-1:

    - ```cmd
        git clone git@github.com:jpsiyyadri/az_speech_translator.git
    ```

    - ```cmd
        cd az_speech_translator
    ```

Step-2:

    - Go to `https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/SpeechServices`

    - Create a `speech resource` and open the resource

    - Copy `REGION` and `SUBSCRIPTION_KEY`

    - Paste it in the `Dockerfile`

Step-3:

    - ```cmd
        docker build -t az_speech_translator .
    ```

    - ```cmd
        docker run -d -p 8501:8501 az_speech_translator
    ```

Step-3:

    - Access your app here: `http://localhost:8501/`

Author: JP Siyyadri <jpsiyyadri@gmail.com>
