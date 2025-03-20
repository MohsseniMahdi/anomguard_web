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
image_path = os.path.join(script_dir, 'assets', 'anom.png')
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


     # Define file paths
    sample_x_test_path = os.path.join(script_dir, 'assets', 'X_test.csv')
    sample_y_test_path = os.path.join(script_dir, 'assets', 'y_test.csv')

    # Custom CSS to position buttons at the bottom left
    st.markdown(
        """
        <style>
            .bottom-left-container {
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 1000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .download-icon-button {
                background: none;
                border: none;
                cursor: pointer;
                font-size: 24px;
                display: flex;
                align-items: center;
                gap: 10px;
                color: white;
            }

                        /* Tooltip styling */
            .download-icon-button .tooltip {
                visibility: hidden;
                width: 160px;
                background-color: black;
                color: white;
                text-align: center;
                padding: 5px;
                border-radius: 5px;
                position: absolute;
                left: 50px; /* Moves the tooltip to the right */
                top: 50%; /* Aligns it in the middle */
                transform: translateY(-50%); /* Centers vertically */
                font-size: 14px;
                opacity: 0;
                transition: opacity 0.3s, left 0.3s;
                white-space: nowrap;
            }
            .download-icon-button:hover .tooltip {
                visibility: visible;
                opacity: 1;
                left: 60px; /* Moves slightly further on hover */
            }
        </style>

        <div class="bottom-left-container">
            <a href="X_test.csv" download="sample_x_test.csv">
                <button class="download-icon-button">📥
                    <span class="tooltip">Download Non-Fraud Data</span>
                </button>
            </a>
            <a href="y_test.csv" download="sample_y_test.csv">
                <button class="download-icon-button">⚠️
                    <span class="tooltip">Download Fraud Data</span>
                </button>
            </a>
            <a href="y_test.csv" download="sample_mixed_test.csv">
                <button class="download-icon-button">🔄
                    <span class="tooltip">Download Mixed Data</span>
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    # Actual file downloads for Streamlit buttons
    # with open(sample_x_test_path, "rb") as f:
    #     st.download_button(label="📥 Not Fraud Transactions",
    #                        data=f,
    #                        file_name="sample_x_test.csv",
    #                        mime="text/csv",
    #                        key="not_fraud_btn")

    # with open(sample_y_test_path, "rb") as f:
    #     st.download_button(label="⚠️ Fraud Sample Test File",
    #                        data=f,
    #                        file_name="sample_y_test.csv",
    #                        mime="text/csv",
    #                        key="fraud_btn")

    # with open(sample_y_test_path, "rb") as f:
    #     st.download_button(label="🔄 Mixed Sample Test File",
    #                        data=f,
    #                        file_name="sample_mixed_test.csv",
    #                        mime="text/csv",
    #                        key="mixed_btn")


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
                loading_message = st.empty()
                loading_message.markdown("⏳ **Processing... Please wait!**")
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
                    loading_message.markdown("✅ **Processing Complete!**")

                except requests.exceptions.JSONDecodeError:
                    st.session_state.response_message = "Failed to decode JSON from response."
                    loading_message.markdown("❌ **Error: Failed to decode response!**")
                except Exception as e:
                    st.session_state.response_message = f"An unexpected error occurred: {e}"
                    loading_message.markdown("❌ **Error: Something went wrong!**")

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
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    if st.session_state.file is not None and st.session_state.result is not None:
        y_test = pd.read_csv(st.session_state.file)

        recall_logreg_prepro = recall_score(y_test['Class'], st.session_state.result)

        predictions = st.session_state.result

            # Create DataFrame for Table
        df_results = pd.DataFrame({
            "Row num": range(1, len(predictions) + 1),
            "Status": ["Fraud" if p == 1 else "Not Fraud" for p in predictions]
        })


        csv_data = convert_df_to_csv(df_results)

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
            <br>
            <a href="data:file/csv;base64,{base64.b64encode(csv_data).decode()}" download="fraud_detection_results.csv">
                <button style="
                    color: black;
                    border: none;
                    padding: 10px 20px;
                    font-size: 18px;
                    border-radius: 5px;
                    cursor: pointer;
                ">
                    📥 Download Predictions
                </button>
            </a>
        """
        result_html += "</div>"
        st.markdown(result_html, unsafe_allow_html=True)

    if st.session_state.result is not None and st.session_state.x_test_file is None:

        predictions = st.session_state.result

        # Create DataFrame for Table
        df_results = pd.DataFrame({
            "Row num": range(1, len(predictions) + 1),
            "Status": ["Fraud" if p == 1 else "Not Fraud" for p in predictions]
        })





elif page == "Heros":
    # st.write("## hero Section")
 # CSS for white box, centering content, and improving layout

    def encode_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    manju_img = encode_image("assets/manju.jpeg")
    kanishk_img = encode_image("assets/Kanishk.jpeg")
    mahdi_img = encode_image("assets/Mahdi.jpeg")
    liubov_img = encode_image("assets/Liubov.jpeg")
    milan_img = encode_image("assets/Milan.jpeg")

    team_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
          .team-container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            width: 85%;
            margin: auto;
            text-align: center;
          }}
          .team-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
          }}
          .team-member {{
            display: flex;
            align-items: center;
            text-align: left;
            gap: 15px;
            background: #f9f9f9;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
          }}
          .team-member img {{
            border-radius: 10px;
            width: 80px;
            height: 80px;
            object-fit: cover;
            border: 2px solid #ddd;
          }}
          .team-info {{
            flex: 1;
          }}
          .team-name {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
          }}
          .team-member.full-width {{
            width: 60%;
            margin: auto;
          }}
          @media (max-width: 768px) {{
            .team-grid {{
              grid-template-columns: 1fr;
            }}
            .team-member {{
              width: 100%;
            }}
            .team-member.full-width {{
              width: 100%;
            }}
          }}
        </style>
    </head>
    <body>
        <div class="team-container">
            <div class="team-grid">
                <div class="team-member">
                   <img src="data:image/jpeg;base64,{liubov_img}" alt="Liubov Zakharchenko" />
                    <div class="team-info">
                        <div class="team-name">Liubov Zakharchenko</div>
                        <p>I used to run my own business in seismic equipment distribution. Now, I want to learn Data Science to restart my career.</p>
                    </div>
                </div>
                <div class="team-member">
                    <img src="data:image/jpeg;base64,{kanishk_img}" alt="Kanishk Waghmare" />
                    <div class="team-info">
                        <div class="team-name">Kanishk Waghmare</div>
                        <p>My name is Kanishk. I am almost done with my PhD in Cognitive Neurosciences from the VU Amsterdam. I am interested in honing my data skills and becoming a Data Scientist.</p>
                    </div>
                </div>
                <div class="team-member">
                <img src="data:image/jpeg;base64,{milan_img}" alt="Milan Martonfi" />
                <div class="team-info">
                    <div class="team-name">Milan Martonfi</div>
                    <p>I have a Master's degree in Sociology. My career includes experience in PR, marketing, communication, media monitoring. media analysis and logistics. Now I’m eager for a new challenge, diving into data science.</p>
                </div>
                </div>
                <div class="team-member">
                    <img src="data:image/jpeg;base64,{manju_img}" alt="Manju Prem" />
                    <div class="team-info">
                        <div class="team-name">Manju Prem</div>
                        <p>With a Master's degree in Computer Applications and 5 years of experience as a Frontend Developer, I am now transitioning into Data Science, following my long-standing passion.</p>
                    </div>
                </div>
            </div>
            <div class="team-member full-width">
                <img src="data:image/jpeg;base64,{mahdi_img}" alt="Mahdi Mohsseni" />
                <div class="team-info">
                    <div class="team-name">Mahdi Mohsseni</div>
                    <p>I hold a PhD in Physics specializing in Optics and Lasers. I spent years as a professor and researcher, now transitioning into Data Science.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Render the HTML inside Streamlit
    components.html(team_html, height=600)

    def encode_video(video_path):
        with open(video_path, "rb") as vid_file:
            return base64.b64encode(vid_file.read()).decode()

    # Encode .mov video file
    video_base64 = encode_video("assets/memories_compressed.mp4")  # Ensure your .mov file is in 'assets' folder

    video_path = os.path.abspath("assets/memories_compressed.mp4")
    st.video(video_path)


elif page == "Faq":
    st.write("## Faq")
    sample_x_test_path = os.path.join(script_dir, 'assets', 'X_test.csv')
    sample_y_test_path = os.path.join(script_dir, 'assets', 'y_test.csv')

    # Load files and create download buttons

    button_html = """
        <div class="download-box">
            <p class="download-text">📂 Download the sample files to test AnomGuard in action!</p>
            <div class="button-container">
                <a href="X_test.csv" download="sample_x_test.csv">
                    <button class="download-button">📥 Not Fraud Transactions</button>
                </a>
                <a href="y_test.csv" download="sample_y_test.csv">
                    <button class="download-button">📥 Fraud Sample Test File</button>
                </a>
                <a href="y_test.csv" download="sample_mixed_test.csv">
                    <button class="download-button">📥 Mixed Sample Test File</button>
                </a>
            </div>
        </div>
        <style>
            .download-box {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                width: 50%;
                text-align: center;
                margin: auto;
            }
            .download-text {
                font-size: 20px;
                font-weight: bold;
                color: black;
                margin-bottom: 15px;
            }
            .button-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
            }
            .download-button {
                color: white;
                border: none;
                padding: 10px 15px;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
                color: black;
            }
            .download-button:hover {
                background-color: #0056b3;
            }
        </style>
    """

    # Display the styled box with buttons
    st.markdown(button_html, unsafe_allow_html=True)

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
    .st-emotion-cache-wq5ihp {
        font-family: "Source Sans Pro", sans-serif;
        font-size: 1.875rem;
        color: inherit;
    }
    /* Adjust the file drop area */
    div[data-testid="stFileDropzone"] {
        min-height: 200px !important; /* Adjust the height */
        padding: 20px !important;
    }
    .st-emotion-cache-ocqkz7 {
                background-color: white;

            }

    </style>
    """,
    unsafe_allow_html=True,
)
