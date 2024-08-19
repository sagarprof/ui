

# import streamlit as st
# import pandas as pd
# import openpyxl
# import os
# import uuid
# from datetime import datetime
# import diff_viewer

# st.set_page_config(layout="wide")
# # Define the repository folder
# REPO_FOLDER = "repo"
# os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists

# # Function to delete the file from the folder based on file_name
# def delete_file(file_name):
#     file_path = os.path.join(REPO_FOLDER, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#         return True
#     return False

# # Calculate metrics for main page colour boxes
# def calculate_metrics():
#     df = pd.read_excel('scores.xlsx')
#     total_rules = len(df)
#     average_score = df['euclidean_score'].mean()
    
#     red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
#     amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
#     green_count = df[df['euclidean_score'] > 0.85].shape[0]
    
#     return total_rules, average_score, red_count, amber_count, green_count



# # Function to load data from 'repo.xlsx'
# def load_repo_data():
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     if os.path.exists(file_path):
#         return pd.read_excel(file_path)
#     # Return a DataFrame with the correct columns if the file does not exist
#     return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

# # Function to refresh the data
# def refresh_data():
#     st.session_state['df'] = load_repo_data() 

# # Function to save data to 'repo.xlsx'
# def save_repo_data(df):
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     df.to_excel(file_path, index=False)

# # Function to update repo data with new file information
# def update_repo_data(file_name, status):
#     df_repo = load_repo_data()
#     new_row = pd.DataFrame([{
#         "job_id": str(uuid.uuid4()),  # Generate a unique job_id
#         "file_name": file_name,
#         "job_status": status,
#         "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "updated_at": ""
#     }])
#     df_repo = pd.concat([df_repo, new_row], ignore_index=True)
#     save_repo_data(df_repo)

# # Dialog box and function
# def details(df):
#     with st.container(height=500, border=True):
#         st.subheader('Filtered Dataframe')
#         st.dataframe(df, use_container_width=True, hide_index=True)
#         tru = filtered_df['truth'].iloc[0]
#         res = filtered_df['response'].iloc[0]
#         st.write("Difference between response and truth")
#         diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# # Initialize or clear session state
# if 'file_data' not in st.session_state:
#     st.session_state['file_data'] = []
#     st.session_state['selected_file'] = None
#     st.session_state['current_tab'] = "Chatbot"  # Initial tab
#     st.session_state['df'] = pd.DataFrame()  # Initialize DataFrame

# # Initial display
# st.title('Insights')
# tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

# # Sidebar for file upload
# st.sidebar.title("Upload Excel Files")
# with st.sidebar.expander("Upload Here"):
#     uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# # Save files and update 'repo.xlsx'
# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with st.spinner(f"Uploading {uploaded_file.name}"):  # Show spinner while uploading
#             file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
#             if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.session_state['file_data'].append({
#                     "file_name": uploaded_file.name,
#                     "job_status": "initiated"
#                 })
#                 update_repo_data(uploaded_file.name, "initiated")  # Log the file information
#                 st.session_state['file_data'][-1]['job_status'] = "✅"

# # Convert the file data to a DataFrame
# if st.session_state['file_data']:
#     df_files = load_repo_data()

#     # Display the DataFrame in the sidebar
#     st.sidebar.subheader("Uploaded files")
#     with st.sidebar:
#         col_sidebar1, col_sidebar2 = st.columns([8, 1])
#         with col_sidebar1:
#             st.write('')

#         with col_sidebar2:
#             if st.button('↻', key='refresh_button'):
#                 refresh_data()

#     selected_file = st.sidebar.dataframe(df_files, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#     if selected_row := selected_file.selection.rows:
#         new_df = df_files.iloc[selected_row]
#         selected_file = new_df['file_name'].iloc[0]

#         # Store the selected file in session state
#         st.session_state['selected_file'] = selected_file
#         if st.sidebar.button('Delete file'):
#             if delete_file(selected_file):
#                 st.success(f"File '{selected_file}' deleted successfully.")
#                 refresh_data()

# # Update current_tab based on user interaction 
# if st.sidebar.visible:
#     st.session_state['current_tab'] = "Metrics"  
# else:
#     st.session_state['current_tab'] = "Chatbot"  

# current_tab = st.session_state['current_tab']

# if current_tab == "Chatbot":
#     with tab1:
#         st.write('chatbot')
# else:
#     with tab2:
#         st.header(":red[Metrics Page]")

#         # Calculate metrics
#         total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()
        
#         # Define colors for the metric boxes
#         colors = {
#             "Total Rules": "lightblue",
#             "Average": "lightgreen",
#             "Red": "red",
#             "Amber": "orange",
#             "Green": "green"
#         }
        
#         # Display metrics with custom HTML and CSS
#         st.markdown(f"""
#         <style>
#         .metric-box {{
#             border-radius: 10px;
#             padding: 20px;
#             margin: 10px;
#             color: white;
#             font-size: 20px;
#             text-align: center;
#             font-weight: bold;
#             width: 150px;  /* Set a fixed width */
#             height: 100px; /* Set a fixed height */
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             box-sizing: border-box;
#         }}
#         </style>
#         """, unsafe_allow_html=True)
        
#         # Layout with uniform boxes
#         col1, col2, col3, col4, col5 = st.columns(5)
        
#         with col1:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Total Rules']}">
#                 Total Rules<br>{total_rules}
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Average']}">
#                 Average<br>{average_score:.2f}
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col3:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Red']}">
#                 Red<br>{red_count}
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col4:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Amber']}">
#                 Amber<br>{amber_count}
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col5:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Green']}">
#                 Green<br>{green_count}
#             </div>
#             """, unsafe_allow_html=True)

#         # Display the selected file content
#         if 'selected_file' in st.session_state and st.session_state['selected_file']:
#             file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
#             df = pd.read_excel(file_path)
#             st.write(f"Content of {st.session_state['selected_file']}:")
#             st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

#             with st.container(height=300):
#                 event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#             df2 = df.copy()
#             df2['score_x'] = df['score'] * 2
#             df2['score_y'] = df['score'] * 3
#             df2['score_z'] = df['score'] * 4

#             if row := event.selection.rows:
#                 find_row = event.selection.rows
#                 filtered_df = df2.iloc[find_row]
#                 details(filtered_df)

# ===========================================================
# graceful deletion
# =========================================================
# import streamlit as st
# import pandas as pd
# import openpyxl
# import os
# import uuid
# from datetime import datetime
# import diff_viewer

# st.set_page_config(layout="wide")
# REPO_FOLDER = "repo"
# os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists   


# def delete_file(file_name):
#     file_path = os.path.join(REPO_FOLDER, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#         return True
#     return False

# def calculate_metrics():
#     try:
#         df = pd.read_excel('scores.xlsx')
#         total_rules = len(df)
#         average_score = df['euclidean_score'].mean()
        
#         red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
#         amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
#         green_count = df[df['euclidean_score'] > 0.85].shape[0]
        
#         return total_rules, average_score, red_count, amber_count, green_count
#     except FileNotFoundError:
#         return 0, 0, 0, 0, 0

# def load_repo_data():
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     if os.path.exists(file_path):
#         return pd.read_excel(file_path)
#     return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

# def refresh_data():
#     st.session_state['df'] = load_repo_data()

# def save_repo_data(df):
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     df.to_excel(file_path, index=False)

# def update_repo_data(file_name, status):
#     df_repo = load_repo_data()
#     new_row = pd.DataFrame([{
#         "job_id": str(uuid.uuid4()),
#         "file_name": file_name,
#         "job_status": status,
#         "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "updated_at": ""
#     }])
#     df_repo = pd.concat([df_repo, new_row], ignore_index=True)
#     save_repo_data(df_repo)

# def details(df):
#     with st.container(height=500, border=True):
#         st.subheader('Filtered Dataframe')
#         st.dataframe(df, use_container_width=True, hide_index=True)
#         tru = filtered_df['truth'].iloc[0]
#         res = filtered_df['response'].iloc[0]
#         st.write("Difference between response and truth")
#         diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# if 'file_data' not in st.session_state:
#     st.session_state['file_data'] = []
#     st.session_state['selected_file'] = None
#     st.session_state['current_tab'] = "Chatbot"
#     st.session_state['df'] = pd.DataFrame()

# st.title('Insights')
# tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

# st.sidebar.title("Upload Excel Files")
# with st.sidebar.expander("Upload Here"):
#     uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with st.spinner(f"Uploading {uploaded_file.name}"):
#             file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
#             if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.session_state['file_data'].append({
#                     "file_name": uploaded_file.name,
#                     "job_status": "initiated"
#                 })
#                 update_repo_data(uploaded_file.name, "initiated")
#                 st.session_state['file_data'][-1]['job_status'] = "✅"

# if st.session_state['file_data']:
#     df_files = load_repo_data()

#     st.sidebar.subheader("Uploaded files")
#     with st.sidebar:
#         col_sidebar1, col_sidebar2 = st.columns([8, 1])
#         with col_sidebar1:
#             st.write('')

#         with col_sidebar2:
#             if st.button('↻', key='refresh_button'):
#                 refresh_data()

#     selected_file = st.sidebar.dataframe(df_files, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#     if selected_row := selected_file.selection.rows:
#         new_df = df_files.iloc[selected_row]
#         selected_file = new_df['file_name'].iloc[0]

#         st.session_state['selected_file'] = selected_file
#         if st.sidebar.button('Delete file'):
#             if delete_file(selected_file):
#                 st.sidebar.success(f"File '{selected_file}' deleted successfully.")
#                 refresh_data()
#                 st.session_state['selected_file'] = None  # Clear the selected file

# if st.sidebar.visible:
#     st.session_state['current_tab'] = "Metrics"
# else:
#     st.session_state['current_tab'] = "Chatbot"

# current_tab = st.session_state['current_tab']

# if current_tab == "Chatbot":
#     with tab1:
#         st.write('chatbot')
# else:
#     with tab2:
#         st.header(":red[Metrics Page]")

#         total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()

#         colors = {
#             "Total Rules": "lightblue",
#             "Average": "lightgreen",
#             "Red": "red",
#             "Amber": "orange",
#             "Green": "green"
#         }

#         st.markdown(f"""
#         <style>
#         .metric-box {{
#             border-radius: 10px;
#             padding: 20px;
#             margin: 10px;
#             color: white;
#             font-size: 20px;
#             text-align: center;
#             font-weight: bold;
#             width: 150px;
#             height: 100px;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             box-sizing: border-box;
#         }}
#         </style>
#         """, unsafe_allow_html=True)

#         col1, col2, col3, col4, col5 = st.columns(5)

#         with col1:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Total Rules']}">
#                 Total Rules<br>{total_rules}
#             </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Average']}">
#                 Average<br>{average_score:.2f}
#             </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Red']}">
#                 Red<br>{red_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col4:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Amber']}">
#                 Amber<br>{amber_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col5:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Green']}">
#                 Green<br>{green_count}
#             </div>
#             """, unsafe_allow_html=True)

#         if 'selected_file' in st.session_state and st.session_state['selected_file']:
#             file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
#             if os.path.exists(file_path):
#                 df = pd.read_excel(file_path)
#                 st.write(f"Content of {st.session_state['selected_file']}:")
#                 st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

#                 with st.container(height=300):
#                     event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#                 df2 = df.copy()
#                 df2['score_x'] = df['score'] * 2
#                 df2['score_y'] = df['score'] * 3
#                 df2['score_z'] = df['score'] * 4

#                 if row := event.selection.rows:
#                     find_row = event.selection.rows
#                     filtered_df = df2.iloc[find_row]
#                     details(filtered_df)
#             else:
#                 st.warning("Selected file does not exist.")
#                 st.session_state['selected_file'] = None
# =====================================================
# added delete from excel file support- issue- new uploads are not shown in the excel
# =====================================================
# import streamlit as st
# import pandas as pd
# import openpyxl
# import os
# import uuid
# from datetime import datetime
# import diff_viewer

# st.set_page_config(layout="wide")
# REPO_FOLDER = "repo"
# os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists   

# def delete_file(file_name):
#     file_path = os.path.join(REPO_FOLDER, file_name)
    
#     # Delete the file if it exists
#     if os.path.isfile(file_path):
#         os.remove(file_path)
    
#     # Remove the file entry from the Excel file
#     df_repo = load_repo_data()
#     df_repo = df_repo[df_repo['file_name'] != file_name]
#     save_repo_data(df_repo)
#     return True

# def calculate_metrics():
#     try:
#         df = pd.read_excel('scores.xlsx')
#         total_rules = len(df)
#         average_score = df['euclidean_score'].mean()
        
#         red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
#         amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
#         green_count = df[df['euclidean_score'] > 0.85].shape[0]
        
#         return total_rules, average_score, red_count, amber_count, green_count
#     except FileNotFoundError:
#         return 0, 0, 0, 0, 0

# def load_repo_data():
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     if os.path.exists(file_path):
#         return pd.read_excel(file_path)
#     return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

# def refresh_data():
#     st.session_state['df'] = load_repo_data()

# def save_repo_data(df):
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     df.to_excel(file_path, index=False)

# def update_repo_data(file_name, status):
#     df_repo = load_repo_data()
#     new_row = pd.DataFrame([{
#         "job_id": str(uuid.uuid4()),
#         "file_name": file_name,
#         "job_status": status,
#         "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "updated_at": ""
#     }])
#     df_repo = pd.concat([df_repo, new_row], ignore_index=True)
#     save_repo_data(df_repo)

# def details(df):
#     with st.container(height=500, border=True):
#         st.subheader('Filtered Dataframe')
#         st.dataframe(df, use_container_width=True, hide_index=True)
#         tru = filtered_df['truth'].iloc[0]
#         res = filtered_df['response'].iloc[0]
#         st.write("Difference between response and truth")
#         diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# if 'file_data' not in st.session_state:
#     st.session_state['file_data'] = []
#     st.session_state['selected_file'] = None
#     st.session_state['current_tab'] = "Chatbot"
#     st.session_state['df'] = pd.DataFrame()

# st.title('Insights')
# tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

# st.sidebar.title("Upload Excel Files")
# with st.sidebar.expander("Upload Here"):
#     uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with st.spinner(f"Uploading {uploaded_file.name}"):
#             file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
#             if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.session_state['file_data'].append({
#                     "file_name": uploaded_file.name,
#                     "job_status": "initiated"
#                 })
#                 update_repo_data(uploaded_file.name, "initiated")
#                 st.session_state['file_data'][-1]['job_status'] = "✅"

# if st.session_state['file_data']:
#     df_files = load_repo_data()

#     st.sidebar.subheader("Uploaded files")
#     with st.sidebar:
#         col_sidebar1, col_sidebar2 = st.columns([8, 1])
#         with col_sidebar1:
#             st.write('')

#         with col_sidebar2:
#             if st.button('↻', key='refresh_button'):
#                 refresh_data()

#     selected_file = st.sidebar.dataframe(df_files, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#     if selected_row := selected_file.selection.rows:
#         new_df = df_files.iloc[selected_row]
#         selected_file = new_df['file_name'].iloc[0]

#         st.session_state['selected_file'] = selected_file
#         if st.sidebar.button('Delete file'):
#             if delete_file(selected_file):
#                 st.sidebar.success(f"File '{selected_file}' deleted successfully.")
#                 refresh_data()
#                 st.session_state['selected_file'] = None  # Clear the selected file

# if st.sidebar.visible:
#     st.session_state['current_tab'] = "Metrics"
# else:
#     st.session_state['current_tab'] = "Chatbot"

# current_tab = st.session_state['current_tab']

# if current_tab == "Chatbot":
#     with tab1:
#         st.write('chatbot')
# else:
#     with tab2:
#         st.header(":red[Metrics Page]")

#         total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()

#         colors = {
#             "Total Rules": "lightblue",
#             "Average": "lightgreen",
#             "Red": "red",
#             "Amber": "orange",
#             "Green": "green"
#         }

#         st.markdown(f"""
#         <style>
#         .metric-box {{
#             border-radius: 10px;
#             padding: 20px;
#             margin: 10px;
#             color: white;
#             font-size: 20px;
#             text-align: center;
#             font-weight: bold;
#             width: 150px;
#             height: 100px;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             box-sizing: border-box;
#         }}
#         </style>
#         """, unsafe_allow_html=True)

#         col1, col2, col3, col4, col5 = st.columns(5)

#         with col1:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Total Rules']}">
#                 Total Rules<br>{total_rules}
#             </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Average']}">
#                 Average<br>{average_score:.2f}
#             </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Red']}">
#                 Red<br>{red_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col4:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Amber']}">
#                 Amber<br>{amber_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col5:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Green']}">
#                 Green<br>{green_count}
#             </div>
#             """, unsafe_allow_html=True)

#         if 'selected_file' in st.session_state and st.session_state['selected_file']:
#             file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
#             if os.path.exists(file_path):
#                 df = pd.read_excel(file_path)
#                 st.write(f"Content of {st.session_state['selected_file']}:")
#                 st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

#                 with st.container(height=300):
#                     event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#                 df2 = df.copy()
#                 df2['score_x'] = df['score'] * 2
#                 df2['score_y'] = df['score'] * 3
#                 df2['score_z'] = df['score'] * 4

#                 if row := event.selection.rows:
#                     find_row = event.selection.rows
#                     filtered_df = df2.iloc[find_row]
#                     details(filtered_df)
#             else:
#                 st.warning("Selected file does not exist.")
#                 st.session_state['selected_file'] = None
# =====================================================================
# solving issue of no new uploads are added to the excel 
# ======================================================================
# import streamlit as st
# import pandas as pd
# import openpyxl
# import os
# import uuid
# from datetime import datetime
# import diff_viewer

# st.set_page_config(layout="wide")
# REPO_FOLDER = "repo"
# os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists   

# # with dialog box and function
# # @st.dialog("Are you sure?",width='small')
# # def delete_file(file_name):
# #     if st.button('Ok'):
# #         file_path = os.path.join(REPO_FOLDER, file_name)
# #         with st.status(f"⚠️ Deleting {file_name}..........."):
# #             # file_path = os.path.join(REPO_FOLDER, file_name)
            
# #             # Delete the file from the filesystem
# #             if os.path.isfile(file_path):
# #                 os.remove(file_path)
            
# #             # Remove the file entry from the Excel file
# #             df_repo = load_repo_data()
# #             df_repo = df_repo[df_repo['file_name'] != file_name]
# #             save_repo_data(df_repo)
# #             return True
# # without dialog box     
# def delete_file(file_name):
#     file_path = os.path.join(REPO_FOLDER, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#     df_repo = load_repo_data()
#     df_repo = df_repo[df_repo['file_name'] != file_name]
#     save_repo_data(df_repo)
#     return True

    

# def calculate_metrics():
#     try:
#         df = pd.read_excel('scores.xlsx')
#         total_rules = len(df)
#         average_score = df['euclidean_score'].mean()
        
#         red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
#         amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
#         green_count = df[df['euclidean_score'] > 0.85].shape[0]
        
#         return total_rules, average_score, red_count, amber_count, green_count
#     except FileNotFoundError:
#         return 0, 0, 0, 0, 0

# def load_repo_data():
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     if os.path.exists(file_path):
#         return pd.read_excel(file_path)
#     return pd.DataFrame(columns=['job_id', 'file_name', 'job_status', 'uploaded_at', 'updated_at'])

# def save_repo_data(df):
#     file_path = os.path.join(REPO_FOLDER, 'repo.xlsx')
#     df.to_excel(file_path, index=False)

# def update_repo_data(file_name, status):
#     df_repo = load_repo_data()
#     new_row = pd.DataFrame([{
#         "job_id": str(uuid.uuid4()),
#         "file_name": file_name,
#         "job_status": status,
#         "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "updated_at": "NA"  # Gap filler
#     }])
#     df_repo = pd.concat([df_repo, new_row], ignore_index=True)
#     save_repo_data(df_repo)

# def refresh_data():
#     st.session_state['df'] = load_repo_data()

# def details(df):
#     with st.container(height=500, border=True):
#         st.subheader('Filtered Dataframe')
#         st.dataframe(df, use_container_width=True, hide_index=True)
#         tru = filtered_df['truth'].iloc[0]
#         res = filtered_df['response'].iloc[0]
#         st.write("Difference between response and truth")
#         diff = diff_viewer.diff_viewer(old_text=res, new_text=tru, lang='none')

# # Initialize session state
# if 'file_data' not in st.session_state:
#     st.session_state['file_data'] = []
#     st.session_state['selected_file'] = None
#     st.session_state['current_tab'] = "Chatbot"
#     st.session_state['df'] = pd.DataFrame()

# st.title('Insights')
# tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

# st.sidebar.title("Upload Excel Files")
# with st.sidebar.expander("Upload Here"):
#     uploaded_files = st.file_uploader("Choose Excel files", accept_multiple_files=True, type=['xlsx', 'xls'])

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with st.spinner(f"Uploading {uploaded_file.name}"):
#             file_path = os.path.join(REPO_FOLDER, uploaded_file.name)
#             if uploaded_file.name not in [file['file_name'] for file in st.session_state['file_data']]:
#                 with open(file_path, "wb") as f:
#                     f.write(uploaded_file.getbuffer())
#                 st.session_state['file_data'].append({
#                     "file_name": uploaded_file.name,
#                     "job_status": "initiated"
#                 })
#                 update_repo_data(uploaded_file.name, "initiated")
#                 st.session_state['file_data'][-1]['job_status'] = "✅"
#                 refresh_data()  # Refresh the data after upload

# if st.session_state['file_data']:
#     df_files = st.session_state['df']

#     st.sidebar.subheader("Uploaded files")
#     with st.sidebar:
#         col_sidebar1, col_sidebar2 = st.columns([8, 1])
#         with col_sidebar1:
#             st.write('')

#         with col_sidebar2:
#             if st.button('↻', key='refresh_button'):
#                 refresh_data()

#     selected_file = st.sidebar.dataframe(df_files, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#     if selected_row := selected_file.selection.rows:
#         new_df = df_files.iloc[selected_row]
#         selected_file_name = new_df['file_name'].iloc[0]

#         # with dialog box

#         # st.session_state['selected_file'] = selected_file_name
#         # if st.sidebar.button('Delete file'):
#         #     if delete_file(selected_file_name):
#         #         # st.sidebar.success(f"File '{selected_file_name}' deleted successfully.")
#         #         refresh_data()  # Refresh the data after deletion
#         #         st.session_state['selected_file'] = None  # Clear the selected file

#         # without dialog box

#         st.session_state['selected_file'] = selected_file_name
#         if st.sidebar.button('Delete file'):
#             if delete_file(selected_file_name):
#                 st.sidebar.success(f"File '{selected_file_name}' deleted successfully.")
#                 refresh_data()  # Refresh the data after deletion
#                 st.session_state['selected_file'] = None  # Clear the selected file

# if st.sidebar.visible:
#     st.session_state['current_tab'] = "Metrics"
# else:
#     st.session_state['current_tab'] = "Chatbot"

# current_tab = st.session_state['current_tab']

# if current_tab == "Chatbot":
#     with tab1:
#         st.write('chatbot')
# else:
#     with tab2:
#         st.header(":red[Metrics Page]")

#         total_rules, average_score, red_count, amber_count, green_count = calculate_metrics()

#         colors = {
#             "Total Rules": "lightblue",
#             "Average": "lightgreen",
#             "Red": "red",
#             "Amber": "orange",
#             "Green": "green"
#         }

#         st.markdown(f"""
#         <style>
#         .metric-box {{
#             border-radius: 10px;
#             padding: 20px;
#             margin: 10px;
#             color: white;
#             font-size: 20px;
#             text-align: center;
#             font-weight: bold;
#             width: 150px;
#             height: 100px;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             box-sizing: border-box;
#         }}
#         </style>
#         """, unsafe_allow_html=True)

#         col1, col2, col3, col4, col5 = st.columns(5)

#         with col1:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Total Rules']}">
#                 Total Rules<br>{total_rules}
#             </div>
#             """, unsafe_allow_html=True)

#         with col2:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Average']}">
#                 Average<br>{average_score:.2f}
#             </div>
#             """, unsafe_allow_html=True)

#         with col3:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Red']}">
#                 Red<br>{red_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col4:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Amber']}">
#                 Amber<br>{amber_count}
#             </div>
#             """, unsafe_allow_html=True)

#         with col5:
#             st.markdown(f"""
#             <div class="metric-box" style="background-color: {colors['Green']}">
#                 Green<br>{green_count}
#             </div>
#             """, unsafe_allow_html=True)

#         if 'selected_file' in st.session_state and st.session_state['selected_file']:
#             file_path = os.path.join(REPO_FOLDER, st.session_state['selected_file'])
#             if os.path.exists(file_path):
#                 df = pd.read_excel(file_path)
#                 st.write(f"Content of {st.session_state['selected_file']}:")
#                 st.info('Click checkbox for detailed metrics', icon=":material/check_circle:")

#                 with st.container(height=300):
#                     event = st.dataframe(df, use_container_width=True, hide_index=True, on_select="rerun", selection_mode="single-row")

#                 df2 = df.copy()
#                 df2['score_x'] = df['score'] * 2
#                 df2['score_y'] = df['score'] * 3
#                 df2['score_z'] = df['score'] * 4

#                 if row := event.selection.rows:
#                     find_row = event.selection.rows
#                     filtered_df = df2.iloc[find_row]
#                     details(filtered_df)
#             else:
#                 st.warning("Selected file does not exist.")
#                 st.session_state['selected_file'] = None

# ===================================================
# removing checkbox- working delete dialog box
# ===================================================
import streamlit as st
import pandas as pd
import openpyxl
import os
import uuid
from datetime import datetime
import diff_viewer

st.set_page_config(layout="wide")
REPO_FOLDER = "repo"
os.makedirs(REPO_FOLDER, exist_ok=True)  # Ensure the repo folder exists   

# with dialog box and function
@st.dialog(f"❗",width='large')
def delete_file(file_name):
    st.subheader('❗Are you sure do you want to delete {selected_file_name}?')
    if st.button('Ok'):
        file_path = os.path.join(REPO_FOLDER, file_name)
        with st.status(f"⚠️ Deleting {file_name}..........."):
            # file_path = os.path.join(REPO_FOLDER, file_name)
            
            # Delete the file from the filesystem
            if os.path.isfile(file_path):
                os.remove(file_path)
            
            # Remove the file entry from the Excel file
            df_repo = load_repo_data()
            df_repo = df_repo[df_repo['file_name'] != file_name]
            save_repo_data(df_repo)
            st.session_state['selected_file'] = None  # Clear the selected file
                            # st.sidebar.success(f"File '{selected_file_name}' deleted successfully.")
            refresh_data()  # Refresh the data after deletion
                # st.session_state['selected_file'] = None  # Clear the selected file
            st.rerun()
            # return True

# def delete_file(file_name):
#     file_path = os.path.join(REPO_FOLDER, file_name)
#     if os.path.isfile(file_path):
#         os.remove(file_path)
#     df_repo = load_repo_data()
#     df_repo = df_repo[df_repo['file_name'] != file_name]
#     save_repo_data(df_repo)
#     st.session_state['selected_file'] = None  # Clear the selected file
#     return True

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

st.title('Insights')
tab1, tab2 = st.tabs(["Chatbot", "Metrics"])

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

        # without dialog box

        # st.session_state['selected_file'] = selected_file_name
        # if st.sidebar.button('Delete file'):
        #     if delete_file(selected_file_name):
        #         st.sidebar.success(f"File '{selected_file_name}' deleted successfully.")
        #         refresh_data()  # Refresh the data after deletion
        #         st.rerun()  # Trigger a full rerun to clear selection
        
                # with dialog box

        st.session_state['selected_file'] = selected_file_name
        selected_file_name=selected_file_name
        if st.sidebar.button('Delete file'):
            delete_file(selected_file_name)

                    

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









