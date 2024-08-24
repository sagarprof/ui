import streamlit as st
from PIL import Image
# import openai
import time
from streamlit_option_menu import option_menu




# horizontal Menu

selected = option_menu(None, ["APM", "Rules to DTP", "DTP to Rules"], 
    icons=['house', 'cloud-upload', "list-task"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f4f8"},  # Faint blue-gray background
        "icon": {"color": "#ff5722", "font-size": "25px"},  # Orange for icons
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#e0e6ed"},  # Light blue-gray hover
        "nav-link-selected": {"background-color": "#004080", "color": "#ffffff"},  # Softer navy blue for selected link
    }
)




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
st.markdown(f'<h1 class="title">{selected}</h1>', unsafe_allow_html=True)
# ####################################
# if -elif-else block of old code
######################################

# Load environment variables (if needed)
# from dotenv import load_dotenv
# load_dotenv()

# Initialize OpenAI API
api_key ='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'

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

