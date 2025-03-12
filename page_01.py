import streamlit as st
import pandas as pd
from io import StringIO

def show_page():
    st.write("### Welcome to Page 1 (Main Page)")

    # File Upload Section (Drag & Drop)
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], accept_multiple_files=False)

    if uploaded_file:
        # Read the uploaded CSV file
        dataframe = pd.read_csv(uploaded_file)

        # Store the dataframe in session state
        st.session_state['uploaded_csv'] = dataframe

        # Display the uploaded CSV content
        st.write("### Uploaded DataFrame:")
        st.dataframe(dataframe)

    elif 'uploaded_csv' in st.session_state:
        # If there's an uploaded CSV file in session state, show it
        st.write("### Previously Uploaded DataFrame:")
        st.dataframe(st.session_state['uploaded_csv'])
