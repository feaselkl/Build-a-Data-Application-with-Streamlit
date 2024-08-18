import streamlit as st
import requests
import pandas as pd
import json
import openai
import azure.cognitiveservices.speech as speechsdk
import streamlit_extras.stateful_button as stx
import time

st.set_page_config(layout="wide")

def create_chat_completion(aoai_deployment_name, messages, aoai_endpoint, aoai_key):
    client = openai.AzureOpenAI(
        api_key=aoai_key,
        api_version="2024-06-01",
        azure_endpoint = aoai_endpoint
    )
    # Create and return a new chat completion request
    return client.chat.completions.create(
        model=aoai_deployment_name,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ],
        stream=True
    )

def create_chat_with_data_completion(aoai_deployment_name, messages, aoai_endpoint, aoai_key, search_endpoint, search_key, search_index_name):
    client = openai.AzureOpenAI(
        api_key=aoai_key,
        api_version="2024-06-01",
        azure_endpoint=aoai_endpoint
    )
    # Create and return a new chat completion request
    return client.chat.completions.create(
        model=aoai_deployment_name,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ],
        stream=True,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "index_name": search_index_name,
                        "authentication": {
                            "type": "api_key",
                            "key": search_key
                        }
                    }
                }
            ]
        }
    )

def recognize_from_microphone(speech_key, speech_region, speech_recognition_language="en-US"):
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language=speech_recognition_language
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config)

    done = False

    def handle_final_result(evt):
        all_results.append(evt.result.text)
        print(evt.result.text)

    all_results = []

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print('CLOSING {}'.format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(handle_final_result)
    transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    transcriber.canceled.connect(lambda evt: print('CANCELLED {}'.format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    # Streamlit refreshes the page on each interaction,
    # so a clean start and stop isn't really possible with button presses.
    # Instead, we're constantly updating transcription results, so that way,
    # when the user clicks the button to stop, we can just stop updating the results.
    # This might not capture the final message, however, if the user stops before
    # we receive the message--we won't be able to call the stop event.
    while not done:
        st.session_state.transcription_results = all_results
        time.sleep(1)

    return

def handle_chat_prompt(prompt, deployment_name, aoai_endpoint, aoai_key, search_endpoint, search_key, search_index_name, model_type):
    # Echo the user's prompt to the chat window
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the user's prompt to Azure OpenAI and display the response
    # The call to Azure OpenAI is handled in create_chat_completion()
    # This function loops through the responses and displays them as they come in.
    # It also appends the full response to the chat history.
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        if model_type == "Use base GPT-4 model":
            for response in create_chat_completion(deployment_name, st.session_state.messages, aoai_endpoint, aoai_key):
                if response.choices:
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
        else:
            for response in create_chat_with_data_completion(deployment_name, st.session_state.messages, aoai_endpoint, aoai_key, search_endpoint, search_key, search_index_name):
                if response.choices:
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    st.write(
    """
    # Chat with Data

    This Streamlit dashboard is intended to show off capabilities of Azure OpenAI, including integration with AI Search, Azure Speech Services, and external APIs.
    """
    )

    model_type = st.sidebar.radio(label = "Select an Option", options = ["Use base GPT-4 model", "Use schema-aware GPT-4 model"])
    with st.sidebar:
        speech_to_text = stx.button("Speech to text", key="recording_in_progress")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    aoai_endpoint = st.secrets["aoai"]["endpoint"]
    aoai_key = st.secrets["aoai"]["key"]
    aoai_deployment_name = st.secrets["aoai"]["deployment_name"]

    search_endpoint = st.secrets["search"]["endpoint"]
    search_key = st.secrets["search"]["key"]
    search_index_name = st.secrets["search"]["index_name"]

    speech_region = st.secrets["speech"]["region"]
    speech_key = st.secrets["speech"]["key"]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if speech_to_text:
        recognize_from_microphone(speech_key, speech_region)
    else:
        if ('transcription_results' in st.session_state):
            speech_contents = ' '.join(st.session_state.transcription_results)
            del st.session_state.transcription_results
            handle_chat_prompt(speech_contents, aoai_deployment_name, aoai_endpoint, aoai_key, search_endpoint, search_key, search_index_name, model_type)

    # Await a user message and handle the chat prompt when it comes in.
    if prompt := st.chat_input("Enter a message:"):
        handle_chat_prompt(prompt, aoai_deployment_name, aoai_endpoint, aoai_key, search_endpoint, search_key, search_index_name, model_type)

if __name__ == "__main__":
    main()
