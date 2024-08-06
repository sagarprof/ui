 
# ------------------------------------------------------------------------
# containerised dataframes on the same page
# broader view
# -------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import openpyxl
import diff_viewer
import random
import time
import os
st.set_page_config(layout="wide")

# Function to create a new folder with a timestamp
def create_folder():
    folder_name = time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

# Initialize or clear session state
if 'file_data' not in st.session_state:
    st.session_state['file_data'] = []
    st.session_state['folder_name'] = ""
    st.session_state['selected_file'] = None
    st.session_state['current_tab'] = "Chatbot"  # Initial tab

# initial display
st.title('Insights')
tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

# dialog box and function
# @st.dialog("Detailed Metrics",width='large')
def details(df):
        with st.container(height=500):
            st.subheader('Filtered Dataframe')
            st.dataframe(
                df,
                # column_config=column_configuration,
                use_container_width=True,
                hide_index=True,
            )
            tru = filtered_df['truth'].iloc[0]
            res=filtered_df['response'].iloc[0]
            st.write("Difference between response and truth")
            diff=diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')



# Sidebar for file upload
st.sidebar.title("Upload Excel Files")
with st.sidebar.expander("Upload Here"):
    uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# Create a new folder to store the files if files are uploaded
if uploaded_files:
    if not st.session_state['folder_name']:
        st.session_state['folder_name'] = create_folder()

    for uploaded_file in uploaded_files:
        with st.spinner(f"Uploading {uploaded_file.name}"):  # Show spinner while uploading
            # Save each uploaded file to the created folder
            if uploaded_file.name not in [file['Name of the file'] for file in st.session_state['file_data']]:
                file_path = os.path.join(st.session_state['folder_name'], uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.session_state['file_data'].append({
                    "Name of the file": uploaded_file.name,
                    "Status": f"{st.spinner('Uploading...')}  "  # Add spinner to Status
                })
                # Update the status to "✅" after successful upload
                st.session_state['file_data'][-1]['Status'] = "✅"

# Convert the file data to a DataFrame
if st.session_state['file_data']:
    df_files = pd.DataFrame(st.session_state['file_data'])

    # Display the DataFrame in the sidebar
    st.sidebar.subheader("Uploaded files")
    st.sidebar.dataframe(df_files)

    # Corrected code for selectbox:
    selected_file = st.sidebar.selectbox("Select a file to view", df_files['Name of the file'].tolist())  # Convert to list of strings

    # Store the selected file in session state
    st.session_state['selected_file'] = selected_file

# Update current_tab based on user interaction 
if st.sidebar.visible:
    st.session_state['current_tab'] = "Metrics"  
else:
    st.session_state['current_tab'] = "Chatbot"  

current_tab = st.session_state['current_tab']

if current_tab == "Chatbot":
    with tab1:
        st.write('chatbot')
else:
    with tab2:
        st.header(":red[Metrics Page]")
        # Display the selected file content
        if 'selected_file' in st.session_state and st.session_state['selected_file']:
            file_path = os.path.join(st.session_state['folder_name'], st.session_state['selected_file'])
            df = pd.read_excel(file_path)
            st.write(f"Content of {st.session_state['selected_file']}:")
            st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

            with st.container(height=300):
                event = st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    on_select="rerun",
                    selection_mode="single-row",
                )

            df2 = df.copy()
            df2['score_x'] = df['score'] * 2
            df2['score_y'] = df['score'] * 3
            df2['score_z'] = df['score'] * 4

            if row := event.selection.rows:
                find_row = event.selection.rows
                filtered_df = df2.iloc[find_row]
                details(filtered_df)
#-------------------------------------------------------------
