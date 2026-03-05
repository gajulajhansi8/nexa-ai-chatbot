import streamlit as st
import requests
import json

st.set_page_config(page_title="My Free AI Chatbot", page_icon="🤖")

st.title("🤖 My Free AI Chatbot")
st.write("Powered by Llama 3 (Running Locally)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=payload, stream=True)
            for chunk in response.iter_lines():
                if chunk:
                    data = json.loads(chunk)
                    if "response" in data:
                        full_response += data["response"]
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure Ollama is still running in your terminal!")