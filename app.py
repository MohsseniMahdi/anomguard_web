import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import base64
import requests
import os

st.set_page_config(page_title="AnomGuard", layout="wide")


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.9;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Correctly construct the path to the image
script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, 'assets', 'credit_card_fraud.jpg')
set_background(image_path)

# Use option_menu instead of st_navbar
page = option_menu(
    None,  # No title for the menu
    ["Dashboard", "How It Works", "Heros", "Faq", "Profile"],  # Menu options
    icons=["house", "book", "code-slash", "people", "person"],  # Optional icons (add as needed)
    menu_icon="cast",  # Optional menu icon
    default_index=0,  # Default selected page
    orientation="horizontal",  # Display horizontally
)

if page == "Dashboard":
    uploaded_files = st.file_uploader(
        "Choose a CSV file", accept_multiple_files=True
    )
    # Initialize session state to store the response message
    if "response_message" not in st.session_state:
        st.session_state.response_message = None

    if uploaded_files:
        # url = 'https://anomguard.lewagon.ai/predict'
        url = 'https://anomguardapi-472205353902.europe-west1.run.app/predict'
        for uploaded_file in uploaded_files:
            files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
            response = requests.post(url, files=files)
            print(response.json())
            try:

                response_data = response.json()
                if 'prediction' in response_data:
                    predictions = response_data['prediction']
                    if all(p == 0 for p in predictions):
                        st.session_state.response_message = "No Fraud Detected!!!"
                    else:
                        st.session_state.response_message = "Fraud Detected"

            except requests.exceptions.JSONDecodeError:
                st.session_state.response_message = "Failed to decode JSON from response."
            except Exception as e:
              st.session_state.response_message = f"An unexpected error occurred: {e}"

    # Show the response message in a box if it exists

    if st.session_state.response_message:
        if st.session_state.response_message == "No Fraud Detected.":
            message_color = "green"
        else:
            message_color = "red"

        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 100px; width: 50%; margin: 20px auto; background-color: white; border-radius: 10px;">
                <div style="color: {message_color}; font-weight: bold; font-size: 20px; padding: 10px;">
                    {st.session_state.response_message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif page == "How It Works":
    st.write("## Documentation")
elif page == "Heros":
    st.write("## hero Section")
elif page == "Faq":
    st.write("## Faq")
elif page == "Profile":
    st.write("## Profile")

# You can further customize the styling using CSS in streamlit
st.markdown(
    """
    <style>
    /* Navigation Bar Container */
    .st-emotion-cache-1v0mbdj {
        background-color: #333333; /* Dark background */
        padding: 10px 20px; /* Top/bottom, left/right padding */
        border-radius: 0px; /* Remove rounded corners */
        margin-bottom: 20px; /* Add space below the menu */
        width: 100%; /* Make the width full */
        max-width:100%;
    }

    /* Menu Items (Links) */
    .st-emotion-cache-1v0mbdj > ul > li > a {
        color: #FFFFFF; /* White text color */
        font-weight: 500; /* Medium bold */
        padding: 10px 20px; /* More padding around the text */
        border-radius: 5px; /* Rounded corners for menu items */
        transition: background-color 0.3s; /* Smooth background color change on hover */
    }

    /* Hover effect for menu items */
    .st-emotion-cache-1v0mbdj > ul > li > a:hover {
        background-color: #555555; /* Slightly lighter on hover */
    }

    /* Selected Menu Item */
    .st-emotion-cache-1v0mbdj > ul > li > a[aria-selected='true'] {
        background-color: #007bff; /* Blue for the selected item */
        color: white; /* White text for the selected item */
    }

    /* Menu icon*/
    .st-emotion-cache-1v0mbdj > div:nth-child(1){
        display:none;
    }
    div[data-testid="stFileUploader"] {
                width: 50%; /* Adjust the width as needed */
                margin: auto; /* Center the uploader horizontally */
            }

    /* Adjust the file drop area */
    div[data-testid="stFileDropzone"] {
        min-height: 200px !important; /* Adjust the height */
        padding: 20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#  div[data-testid="stFileUploader"] div {
        #     padding: 30px !important;  /* Increase padding */
        # }
