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
import page_06
import page_07
import page_08

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
        margin-bottom: 10px;
    }
    .button-blue:hover {
        background-color: #34495e;
    }
    .left-side-buttons {
        display: flex;
        flex-direction: column;
        position: fixed;
        left: 10px;
        top: 20%;
        z-index: 10;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Define the navigation_bar function
def navigation_bar():
    # Top buttons
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

    # Left-side buttons (Hero section, How it works, FAQ)
    st.markdown('<div class="left-side-buttons">', unsafe_allow_html=True)

    if st.button("Hero Section"):
        st.session_state.page = "hero_section"

    if st.button("How it Works"):
        st.session_state.page = "how_it_works"

    if st.button("FAQ"):
        st.session_state.page = "faq"

    st.markdown('</div>', unsafe_allow_html=True)

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
    elif st.session_state.page == "hero_section":
        page_06.show_page()  # Hero section
    elif st.session_state.page == "how_it_works":
        page_07.show_page()  # How it works
    elif st.session_state.page == "faq":
        page_08.show_page()  # FAQ

if __name__ == "__main__":
    main()
