import streamlit as st
import pandas as pd
import base64
from PIL import Image
from io import BytesIO, StringIO

import page_01
import page_02
import page_03
import page_04
import page_05

# 1. Define CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #282c34; /* Dark gray background for the overall page */
        color: white; /* Default text color */
    }
    .main-content {
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px; /* Add some space between nav and content */
    }
    .button-blue {
        background-color: #2c3e50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .button-blue:hover {
        background-color: #34495e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# In the navigation_bar function
def navigation_bar():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        if st.button("Home"):
            st.session_state.page = "main"

    with col2:
        if st.button("Dashboard"):
            st.session_state.page = "dashboard"

    with col3:
        if st.button("Notifications"):
            st.session_state.page = "notifications"

    with col4:
        if st.button("Reserved"):
            st.session_state.page = "page_05"

    with col5:
        if st.button("Profile"):
            st.session_state.page = "profile"

# 3. Define the main function
def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    navigation_bar()

    st.markdown("### Current Page: " + st.session_state.page)

    if st.session_state.page == "main":
        page_01.show_page()
    elif st.session_state.page == "dashboard":
        page_02.show_page()
    elif st.session_state.page == "profile":
        page_03.show_page()
    elif st.session_state.page == "notifications":
        page_04.show_page()
    elif st.session_state.page == "page_05":
        page_05.show_page()

if __name__ == "__main__":
    main()

# st.write("Upload your document here")

# uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# if uploaded_file is not None:
#    dataframe = pd.read_csv(uploaded_file)
#    st.write("Uploaded DataFrame:", dataframe)

#st.write("Navigation bar")
#st.write("Upload the file here")
