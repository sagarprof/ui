
# ------------------------------------------------------------------------
# variation 1-containerised dataframes on the same page
# broader view
# variation 2- added checkbox in sidebar dataframe 
# -------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import openpyxl
import diff_viewer
import random
import time
import os
st.set_page_config(layout="wide")

# Calculate metrics
def calculate_metrics():
    df = pd.read_excel('scores.xlsx')
    total_rules = len(df)
    average_score = df['euclidean_score'].mean()
    
    red_count = df[(df['euclidean_score'] > 0.10) & (df['euclidean_score'] <= 0.75)].shape[0]
    amber_count = df[(df['euclidean_score'] > 0.75) & (df['euclidean_score'] <= 0.85)].shape[0]
    green_count = df[df['euclidean_score'] > 0.85].shape[0]
    
    return total_rules, average_score, red_count, amber_count, green_count

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
        with st.container(height=500,border=True):
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
    selected_file=st.sidebar.dataframe(df_files,
                        use_container_width=True,
                        hide_index=True,
                        on_select="rerun",
                        selection_mode="single-row",
                        )
    
    if selected_row := selected_file.selection.rows:
        new_df = df_files.iloc[selected_row]
        # st.sidebar.dataframe(new_df)
        
        selected_file=new_df['Name of the file'].iloc[0]
        # st.sidebar.write(selected_file)

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
        col1, col2, col3,col4, col5= st.columns(5)
        
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
