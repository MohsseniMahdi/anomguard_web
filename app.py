import streamlit as st
import pandas as pd
import base64
from PIL import Image
from io import BytesIO, StringIO
import importlib

import page_01
import page_02
import page_03
import page_04
import page_05
import pages.faq
import pages.hero_section
import pages.how_it_works

# Dynamic imports for pages
PAGE_MODULES = {
    "hero_section": "pages.hero_section",
    "how_it_works": "pages.how_it_works",
    "faq": "pages.faq"
}

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
            st.write(f"Switching to: {st.session_state.page}")

    with col2:
        if st.button("Dashboard"):
            st.session_state.page = "dashboard"
            st.write(f"Switching to: {st.session_state.page}")

    with col3:
        if st.button("Notifications"):
            st.session_state.page = "notifications"
            st.write(f"Switching to: {st.session_state.page}")

    with col4:
        if st.button("Reserved"):
            st.session_state.page = "page_05"
            st.write(f"Switching to: {st.session_state.page}")

    with col5:
        if st.button("Profile"):
            st.session_state.page = "profile"
            st.write(f"Switching to: {st.session_state.page}")

    # Left-side buttons (Hero section, How it works, FAQ)
    st.markdown('<div class="left-side-buttons">', unsafe_allow_html=True)

    if st.button("Hero Section"):
        st.session_state.page = "hero_section"
        st.write(f"Switching to: {st.session_state.page}")

    if st.button("How it Works"):
        st.session_state.page = "how_it_works"
        st.write(f"Switching to: {st.session_state.page}")

    if st.button("FAQ"):
        st.session_state.page = "faq"
        st.write(f"Switching to: {st.session_state.page}")

    st.markdown('</div>', unsafe_allow_html=True)

# 3. Define the main function
def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    navigation_bar()

    st.markdown("### Current Page: " + st.session_state.page)

    # Load the page dynamically
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
    elif st.session_state.page in PAGE_MODULES:
        # Dynamically import the page
        module_name = PAGE_MODULES[st.session_state.page]
        page_module = importlib.import_module(module_name)
        page_module.show_page()

if __name__ == "__main__":
    main()
