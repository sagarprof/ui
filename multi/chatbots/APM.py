import streamlit as st
from PIL import Image
import openai
import time

# Load environment variables (if needed)
# from dotenv import load_dotenv
# load_dotenv()

# Initialize OpenAI API
api_key ='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'


st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: red; /* Text color red */

    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app with custom CSS class for the title
st.markdown('<h1 class="title">APM Chatbot</h1>', unsafe_allow_html=True)


# st.title(':red[Chatbot]')

# Load images
jet = Image.open('jetlogo.png')
human = Image.open('yellow.png')

def get_api_response(query):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "Hi human! How can I help you today?"}]

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=jet):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"], avatar=human):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=human):
        st.markdown(prompt)
    
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar=jet):
            with st.spinner("Thinking..."):
                response = get_api_response(prompt)
                answer = ""
                placeholder = st.empty()
                for chunk in response.split():
                    answer += chunk + " "
                    time.sleep(0.08)  # Simulate typing delay
                    placeholder.markdown(answer + "▌")
                st.session_state.messages[-1]["content"] = answer
                # placeholder.empty()
    message = {"role":"assistant", "content":response}
    st.session_state.messages.append(message)

