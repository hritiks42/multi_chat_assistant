from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import streamlit as st
from encryption_test import decrypt
from time import sleep

load_dotenv()


@st.cache_data
def model_connect(user_prompt, llm_name, model_name):
    if llm_name == 'GPT':
        openaikey = st.session_state.OPENAI_API_KEY
        client = OpenAI(api_key=openaikey)

        response = client.responses.create(
            model=model_name,
            input=user_prompt
        )
        return response.output_text
    else:
        claude_key = st.session_state.CLAUDE_API_KEY
        client = Anthropic(api_key=claude_key)
        message = client.messages.create(
            model=model_name,
            max_tokens=8192,
            temperature=1,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )
        return message.content[0].text

    


# if llm_name:
#     st.write(llm_name)
# if models:
#     st.write(models)


@st.dialog("Please enter valid decryption key")
def enter_key_dialog():
    user_ip = st.text_input("KEY")
    if st.button("Submit"):
        try:
            decrypt_resp = decrypt(user_ip)
            st.session_state.OPENAI_API_KEY = decrypt_resp['openai']
            st.session_state.CLAUDE_API_KEY = decrypt_resp['claude']
        except Exception as err:
            st.session_state.decrypt_status = False
            st.warning("Invalid Key")
        else:
            st.success("Valid Key")
            sleep(1)
            st.session_state.decrypt_status = True
            st.rerun()

if hasattr(st.session_state, 'decrypt_status'):
    col1, col2 = st.columns(2)

    with col1:
        llm_name = st.selectbox('LLM Name',('Claude', 'GPT'))

    with col2:
        model_tuple = tuple()
        if llm_name == 'Claude':
            model_tuple = ('claude-opus-4-20250514', 'claude-sonnet-4-20250514', 'claude-3-7-sonnet-latest', 'claude-3-5-haiku-latest')
        else:
            model_tuple = ('gpt-4.1', 'gpt-4.1-mini', 'gpt-4o-mini', 'o4-mini')

        model_name = st.selectbox('Select model', model_tuple)
        
    prompt = st.chat_input("Enter your prompt")
    container = st.container(height=850)
    if prompt:
        container.chat_message("user").write(prompt)
        response = model_connect(prompt, llm_name, model_name)
        container.chat_message("assistant").write(response)
else:
    enter_key_dialog()