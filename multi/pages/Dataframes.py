

import streamlit as st
import pandas as pd
import openpyxl
import os
import uuid
from datetime import datetime
import diff_viewer
import os
import json
from PIL import Image
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import time


st.set_page_config(layout="wide")



# Calculate metrics for main page colour boxes
def calculate_metrics():
    df = pd.read_excel('scores.xlsx')
    total_rules = len(df)
    average_score = df['euclidean_score'].mean()
    
    red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
    amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
    green_count = df[df['euclidean_score'] > 0.85].shape[0]
    
    return total_rules, average_score, red_count, amber_count, green_count

# Define the repository folder
REPO_FOLDER = "repo"
os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists

# Function to load data from 'repo.xlsx'
def load_repo_data():
    file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    # Return a DataFrame with the correct columns if the file does not exist
    return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

# Function to refresh the data
def refresh_data():
    st.session_state['df'] = load_repo_data() 

# Function to save data to 'repo.xlsx'
def save_repo_data(df):
    file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
    df.to_excel(file_path, index=False)

# Function to update repo data with new file information
def update_repo_data(file_name, status):
    df_repo = load_repo_data()
    new_row = pd.DataFrame([{
        "job_id": str(uuid.uuid4()),  # Generate a unique job_id
        "file_name": file_name,
        "job_status": status,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": ""
    }])
    df_repo = pd.concat([df_repo, new_row], ignore_index=True)
    save_repo_data(df_repo)

# Dialog box and function
def details(df):
    with st.container(height=500, border=True):
        st.subheader('Filtered Dataframe')
        st.dataframe(df, use_container_width=True, hide_index=True)
        tru = filtered_df['truth'].iloc[0]
        res = filtered_df['response'].iloc[0]
        st.write("Difference between response and truth")
        diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# Initialize or clear session state
if 'file_data' not in st.session_state:
    st.session_state['file_data'] = []
    st.session_state['selected_file'] = None
    st.session_state['df'] = pd.DataFrame()  # Initialize DataFrame


# Sidebar for file upload
st.sidebar.title("Upload Excel Files")
with st.sidebar.expander("Upload Here"):
    uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# Save files and update 'repo.xlsx'
if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Uploading {uploaded_file.name}"):  # Show spinner while uploading
            file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
            if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state['file_data'].append({
                    "file_name": uploaded_file.name,
                    "job_status": "initiated"
                })
                update_repo_data(uploaded_file.name, "initiated")  # Log the file information
                st.session_state['file_data'][-1]['job_status'] = "✅"

# Convert the file data to a DataFrame
if st.session_state['file_data']:
    df_files = load_repo_data()

    # Display the DataFrame in the sidebar
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
        selected_file = new_df['file_name'].iloc[0]

        # Store the selected file in session state
        st.session_state['selected_file'] = selected_file

st.title(":red[Metrics Page]")


# Calculate metrics
total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()

# Define colors for the metric boxes
colors = {
    "Total Rules": "lightblue",
    "Average": "lightgreen",
    "Red": "red",
    "Amber": "orange",
    "Green": "green"
}

# Display metrics with custom HTML and CSS
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
    width: 150px;  /* Set a fixed width */
    height: 100px; /* Set a fixed height */
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}}
</style>
""", unsafe_allow_html=True)

# Layout with uniform boxes
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

# Display the selected file content
if 'selected_file' in st.session_state and st.session_state['selected_file']:
    file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
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
