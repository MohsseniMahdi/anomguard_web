import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import base64
import requests
import os
from sklearn.metrics import recall_score
import streamlit.components.v1 as components

st.set_page_config(page_title="AnomGuard", layout="wide")

baseUrl = 'https://anomguardapi-472205353902.europe-west1.run.app'

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

page = option_menu(
    None,
    ["Dashboard", "How It Works", "Heros", "Faq", "Profile"],
    icons=["house", "book", "code-slash", "people", "person"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if page == "Dashboard":
    st.session_state.file = None
    st.session_state.x_test_file = None
    st.session_state.result = None
    uploaded_files = st.file_uploader(
        "Choose a CSV file", accept_multiple_files=True
    )
    # Initialize session state to store the response message
    if "response_message" not in st.session_state:
        st.session_state.response_message = None

    if uploaded_files:
        url = f'{baseUrl}/predict'
        # url = 'http://localhost:8000/predict'
        for uploaded_file in uploaded_files:

            if "y_test" in uploaded_file.name:

                st.session_state.file = uploaded_file
            else :
                files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}

                response = requests.post(url, files=files)

                st.session_state.x_test_file = uploaded_file
            try:
                response_data = response.json()
                if 'prediction' in response_data:
                    predictions = response_data['prediction']

                    predictions = [int(p) for p in predictions]
                    count_non_fraud = predictions.count(0)
                    count_fraud = predictions.count(1)
                    fraud_indices = [i + 1 for i, p in enumerate(predictions) if p == 1]
                    st.session_state.result = predictions
                    if fraud_indices:
                    # all(p == 0 for p in predictions):
                        # st.session_state.response_message = "No Fraud Detected."
                        if len(fraud_indices) < 6:

                            st.session_state.response_message = f"{len(fraud_indices)} Fraud transaction(s) found in row number {', '.join(map(str, fraud_indices))}!!!"
                        else:
                            st.session_state.response_message = f"{len(fraud_indices)} Fraud transaction(s) found!!!!"

                    else:
                        st.session_state.response_message = "No Fraud Detected!!!"


            except requests.exceptions.JSONDecodeError:
                st.session_state.response_message = "Failed to decode JSON from response."
            except Exception as e:
              st.session_state.response_message = f"An unexpected error occurred: {e}"

    if st.session_state.response_message:
        if st.session_state.response_message == "No Fraud Detected!!!":
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

    if st.session_state.file is not None and st.session_state.result is not None:
        y_test = pd.read_csv(st.session_state.file)

        recall_logreg_prepro = recall_score(y_test['Class'], st.session_state.result)

        predictions = st.session_state.result

            # Create DataFrame for Table
        df_results = pd.DataFrame({
            "Row num": range(1, len(predictions) + 1),
            "Status": ["Fraud" if p == 1 else "Not Fraud" for p in predictions]
        })

        # Define styling for color-coding
        def highlight_fraud(val):
            color = 'red' if val == "Fraud" else 'green'
            return f'color: {color}; font-weight: bold;'


        result_html = f"""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            width: 50%;
            margin: auto;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        ">
            <p style="color: black; font-size: 24px; font-weight: bold;">
                This model has a Recall Score: {recall_logreg_prepro:.4f}
            </p>
        """
        result_html += "</div>"
        st.markdown(result_html, unsafe_allow_html=True)


        table_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .styled-table {{
                    width: 25%;  /* Set table width */
                    margin: auto;  /* Center table */
                    border-collapse: collapse;
                    font-size: 18px;
                }}
                .styled-table th, .styled-table td {{
                    padding: 10px;
                    text-align: center;
                    border: 1px solid #ddd;
                    background-color: white;

                }}
                .styled-table th:first-child,
                .styled-table td:first-child {{
                    width: 80px;
                    text-align: center;
                }}
                .fraud {{ color: red; font-weight: bold; }}
                .not-fraud {{ color: green; font-weight: bold; }}
            </style>
        </head>
        <body>
        <table class="styled-table" >
            <thead>
                <tr>
                    <th>Row Num</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
        """

        for index, row in df_results.iterrows():
            status_class = "fraud" if row["Status"] == "Fraud" else "not-fraud"
            table_html += f"""
            <tr>
                <td>{row["Row num"]}</td>
                <td class="{status_class}">{row["Status"]}</td>
            </tr>
            """

        table_html += "</tbody></table></body></html>"

        components.html(table_html, height=300)




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
