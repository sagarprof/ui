import streamlit as st
import pandas as pd
import openpyxl
import os
import uuid
from datetime import datetime
import diff_viewer
import time
# import keyboard

st.set_page_config(layout="wide")
REPO_FOLDER = "repo"
os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists 

@st.dialog(" ⛔ Delete Upload",width='small')
def delete_file(selected_file_name):
        # st.divider()
        # st.write("---")
        # ❗🛑 ‼️ 💡🚩♻ ♻️  ⚠
        # https://emojidb.org/delete-emojis
        st.warning(f"Are you sure you want to delete file '{selected_file_name}' ?")
        _,col_dialogN, col_dialogY = st.columns([6,2,2])
        with col_dialogN:
            st.write("")
            # if st.button('No'):
            #     keyboard.press_and_release('esc')

        status_placeholder = st.empty()
        with col_dialogY:

            if st.button('Yes',use_container_width=True):
                file_path = os.path.join(REPO_FOLDER, selected_file_name)
                
                with status_placeholder,st.spinner(f"Deleting {selected_file_name}..."):
                    time.sleep(2)
                    # file_path = os.path.join(REPO_FOLDER, file_name)
                    
                    # Delete the file from the filesystem
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        time.sleep(2)
                    st.success(f"File '{selected_file_name}' deleted successfully.")
                    time.sleep(2)
                    
                    # Remove the file entry from the Excel file
                    df_repo = load_repo_data()
                    df_repo = df_repo[df_repo['file_name'] != selected_file_name]
                    save_repo_data(df_repo)
                    st.session_state['selected_file'] = None  # Clear the selected file
                                    # st.sidebar.success(f"File '{selected_file_name}' deleted successfully.")
                    refresh_data()  # Refresh the data after deletion
                        # st.session_state['selected_file'] = None  # Clear the selected file
                                    # Update the placeholder with a success message
                    st.rerun()


def calculate_metrics():
    try:
        df = pd.read_excel('scores.xlsx')
        total_rules = len(df)
        average_score = df['euclidean_score'].mean()
        
        red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
        amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
        green_count = df[df['euclidean_score'] > 0.85].shape[0]
        
        return total_rules, average_score, red_count, amber_count, green_count
    except FileNotFoundError:
        return 0, 0, 0, 0, 0

def load_repo_data():
    file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

def save_repo_data(df):
    file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
    df.to_excel(file_path, index=False)

def update_repo_data(file_name, status):
    df_repo = load_repo_data()
    new_row = pd.DataFrame([{
        "job_id": str(uuid.uuid4()),
        "file_name": file_name,
        "job_status": status,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "NA"  # Gap filler
    }])
    df_repo = pd.concat([df_repo, new_row], ignore_index=True)
    save_repo_data(df_repo)

def refresh_data():
    st.session_state['df'] = load_repo_data()

def details(df):
    with st.container(height=500, border=True):
        st.subheader('Filtered Dataframe')
        st.dataframe(df, use_container_width=True, hide_index=True)
        tru = filtered_df['truth'].iloc[0]
        res = filtered_df['response'].iloc[0]
        st.write("Difference between response and truth")
        diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# Initialize session state
if 'file_data' not in st.session_state:
    st.session_state['file_data'] = []
    st.session_state['selected_file'] = None
    st.session_state['current_tab'] = "Chatbot"
    st.session_state['df'] = pd.DataFrame()

# Custom CSS to align the title
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
st.markdown('<h1 class="title">Insights</h1>', unsafe_allow_html=True)

# st.title(':red[Insights]')
st.sidebar.title("Upload Excel Files")
with st.sidebar.expander("Upload Here"):
    uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Uploading {uploaded_file.name}"):
            file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
            if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state['file_data'].append({
                    "file_name": uploaded_file.name,
                    "job_status": "initiated"
                })
                update_repo_data(uploaded_file.name, "initiated")
                st.session_state['file_data'][-1]['job_status'] = "✅"
                refresh_data()  # Refresh the data after upload

if st.session_state['file_data']:
    df_files = st.session_state['df']

    st.sidebar.subheader("Uploaded files")
    with st.sidebar:
        col_sidebar1, col_sidebar2 = st.columns([8, 1])
        with col_sidebar1:
            st.write('')

        with col_sidebar2:
            if st.button('↻', key='refresh_button'):
                refresh_data()

    selected_file = st.sidebar.dataframe(df_files, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

    if selected_row := selected_file.selection.rows:
        new_df = df_files.iloc[selected_row]
        selected_file_name = new_df['file_name'].iloc[0]

        st.session_state['selected_file'] = selected_file_name
        with st.sidebar:
            col_delete1,col_delete2 = st.columns([5,2])
            with col_delete1:
                st.write(' ')
            with col_delete2:
                if st.sidebar.button('Delete file'):
                    delete_file(selected_file_name)
                    # delete_file(selected_file_name)

        st.header(":red[Metrics Page]")

        total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()

        colors = {
            "Total Rules": "lightblue",
            "Average": "lightgreen",
            "Red": "red",
            "Amber": "orange",
            "Green": "green"
        }

        st.markdown(f"""
        <style>
        .metric-box {{
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            color: white;
            font-size: 20px;
            text-align: center;
            font-weight: bold;
            width: 150px;
            height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-sizing: border-box;
        }}
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
            <div class="metric-box" style="background-color: {colors['Total Rules']}">
                Total Rules<br>{total_rules}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box" style="background-color: {colors['Average']}">
                Average<br>{average_score:.2f}
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box" style="background-color: {colors['Red']}">
                Red<br>{red_count}
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box" style="background-color: {colors['Amber']}">
                Amber<br>{amber_count}
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div class="metric-box" style="background-color: {colors['Green']}">
                Green<br>{green_count}
            </div>
            """, unsafe_allow_html=True)

        if 'selected_file' in st.session_state and st.session_state['selected_file']:
            file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
            if os.path.exists(file_path):
                df = pd.read_excel(file_path)
                st.write(f"Content of {st.session_state['selected_file']}:")
                st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

                with st.container(height=300):
                    event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

                df2 = df.copy()
                df2['score_x'] = df['score'] * 2
                df2['score_y'] = df['score'] * 3
                df2['score_z'] = df['score'] * 4

                if row := event.selection.rows:
                    find_row = event.selection.rows
                    filtered_df = df2.iloc[find_row]
                    details(filtered_df)
            else:
                st.warning("Selected file does not exist.")
                st.session_state['selected_file'] = None