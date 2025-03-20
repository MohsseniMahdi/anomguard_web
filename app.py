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
        opacity: 1;
        transition: opacity 0.5s ease-in-out;

    }}
     [data-testid="stAppViewContainer"].fade-out {{
        opacity: 0.5; /* Faded opacity */
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
    }}

    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Correctly construct the path to the image
script_dir = os.path.dirname(__file__)
image_path_background = os.path.join(script_dir, 'assets', 'background3.png')
image_path = os.path.join(script_dir, 'assets')
set_background(image_path_background)

page = option_menu(
    None,
    ["Dashboard", "Model Specs", "Docs", "User Manual", "Team"],
    icons=["grid", "bar-chart-line", "file-earmark-text", "book", "people"],
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
    # sample_x_test_path = os.path.join(script_dir, 'assets', 'X_test.csv')
    # sample_y_test_path = os.path.join(script_dir, 'assets', 'y_test.csv')

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
            <a href="X_test.csv" download="X_test_nonfraud.csv">
                <button class="download-icon-button">📥
                    <span class="tooltip">Download Non-Fraud Data</span>
                </button>
            </a>
            <a href="y_test.csv" download="X_test_fraud.csv">
                <button class="download-icon-button">⚠️
                    <span class="tooltip">Download Fraud Data</span>
                </button>
            </a>
            <a href="y_test.csv" download="X_test_mix.csv">
                <button class="download-icon-button">🔄
                    <span class="tooltip">Download Mixed Data</span>
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
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
            <div style="display: flex; justify-content: center; align-items: center; height: 100px; width: 50%; margin: 90px auto 50px auto; background-color: white; border-radius: 10px;">
                <div style="color: {message_color}; font-weight: bold; font-size: 20px; padding: 10px;">
                    {st.session_state.response_message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

elif page == "Model Specs":
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    if st.session_state.result is not None:
        # y_test = pd.read_csv(st.session_state.file)

        # recall_logreg_prepro = recall_score(y_test['Class'], st.session_state.result)

        predictions = st.session_state.result

            # Create DataFrame for Table
        df_results = pd.DataFrame({
            "Row num": range(1, len(predictions) + 1),
            "Status": ["Fraud" if p == 1 else "Not Fraud" for p in predictions]
        })

        csv_data = convert_df_to_csv(df_results)

        result_html = f"""
        <div style="
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            width: 89%;
            margin: auto;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            font-size: 22px;
            font-weight: bold;
        ">
            <p style="color: black; font-size: 24px; font-weight: bold;">
                This model has a Recall Score: 91.66
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


        def encode_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        # Encode images
        graph1_img = encode_image("assets/Learning_Curve.png")
        graph2_img = encode_image("assets/Confusion_Matrix.png")

        # HTML Template to Display Images
        graph_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                .graph-container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    width: 85%;
                    margin: auto;
                    text-align: center;
                }}
                .graph-box {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .graph-img {{
                    border-radius: 10px;
                    width: 70%;
                    object-fit: cover;
                    border: 2px solid #ddd;
                }}
                .graph-title {{
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .graph-description {{
                    font-size: 16px;
                    color: #555;
                    margin-bottom: 20px;
                }}
                </style>
            </head>
            <body>
                <div class="graph-container">
                    <div class="graph-box">
                        <div class="graph-title">Learning Curve Logistic Regression Model</div>
                        <img class="graph-img" src="data:image/png;base64,{graph1_img}" alt="Graph 1"/>
                    </div>
                    <div class="graph-box">
                        <div class="graph-title">Confusion Matrix For Test Dataset </div>
                        <img class="graph-img" src="data:image/png;base64,{graph2_img}" alt="Graph 2"/>
                    </div>
                </div>
            </body>
            </html>
        """

        # Render the HTML inside Streamlit
        components.html(graph_html, height=1500)


elif page == "Docs":


    #Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Introduction",
        "2. ML Workflow",
        "3. Tech Stack ",
        "4. Architecture",
        "6. Key Features",
        "5. Future Improvements"
    ])


    common_style_docs ="""
            <style>
                /* General Styles */
                .st-emotion-cache-wq5ihp {
                    font-family: "Open Sans, sans-serif;
                    font-size: 2.875rem !important;
                    color: inherit;
                }

                .container {
                   background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
                    padding: 10px;
                    border-radius: 12px;
                    box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
                    width: 80%;
                    margin: 20px auto;
                    text-align: justified;
                    font-family: 'Open Sans', sans-serif;
                }

                /* Heading Styles */
                h1 {
                    color: #1f76c9;
                    font-size: 30px;
                    text-align: center;
                }

                h2 {
                    color: #333;
                    font-size: 24px;
                    margin-top: 20px;
                }

                h3 {
                    font-size: 18px;
                    color: #555;
                }

                /* Paragraph Styles */
                p {
                    font-size: 14px;
                    line-height: 1.6;
                    margin-bottom: 10px;
                    display: inline;
                    text-align: justify;
                }

                .tech-item { display: flex; align-items: center; margin-bottom: 20px; }
                .tech-item img { height: 40px; margin-right: 10px; }
                .tech-item span { font-size: 16px; }
                .tech-container { display: flex; flex-wrap: wrap; justify-content: center;}
                .tech-container div { width: 40%; min-width: 250px; margin: 10px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
                /* Tab Styling (Adjust width here) */
                .stTabs[data-baseweb="tab-list"] button {
                    padding: 10px 15px; /* Adjust padding for size */
                    font-size:24px;     /* Adjust font size */
                    font-weight: bold;
                    }
                }

            </style>
        """


    # Tab 1: Introduction

    with tab1:
        introduction_html = f"""
        <html>
        {common_style_docs}
        <body>
            <div class="container">

            <h2>Introduction</h2>
            <p>AnomGuard is a web application designed to detect fraudulent credit card transactions. Utilizing a machine learning model trained on the Kaggle Credit Card Fraud Detection dataset, AnomGuard provides a user-friendly interface for analyzing transaction data.</p>
            <br/>
            <br/>
            <p><strong>Dataset Overview:</strong>The dataset <a href="https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud" target="_blank"> [Kaggle link]</a>features credit card transactions made by European cardholders over a two-day period in September 2013. It contains 284,807 transactions, of which only 492 are fraudulent—approximately 0.172% of the data. This notable class imbalance presents challenges during model training and evaluation, requiring careful attention to ensure fair and reliable model performance.</p>
            <br/>
            <br/>
            <p><strong>Feature Description:</strong>
            <ul><li><p>Time:The time elapsed in seconds between each transaction and the first transaction in the dataset.</p></li>
                <br/>
                <li><p>V1 to V28: Principal components derived from a PCA transformation applied to the original features, anonymized for privacy reasons.</p></li>
                <br/>
                <li><p>Amount: The transaction amount, which can provide insights and be utilized for cost-sensitive learning.</p></li>
                <br/>
                <li><p>Class: The target variable, where 1 indicates a fraudulent transaction, and 0 indicates a legitimate transaction.</p></li>

            <div/>
        </body>
        </html>
        """
        components.html(introduction_html, height=600, scrolling=True)

    with tab2:
        workflow_html = f"""
         <html>
        {common_style_docs}
        <body>
            <div class="container">
            <h2>Workflow</h2>
                <ul>
                <h3>Data Aqcuisition</h3>
                <ul><li><p> Data was loaded in Google Cloud Storage and stored in a table on BigQuery. We cached the data on our local machines for testing and evaulation purposes.</p></li></ul>

                <h3>Preprocessing</h3>
                <ul><li><p>Checked for missing values and removed 1,081 duplicate entries.</p>
                    <li><p>Applied cyclical feature transformation on ‘Time’ for better model interpretation.</p>
                    <li><p>Utilized BorderlineSMOTE to generate synthetic samples for the minority class, addressing the class imbalance.</p>
                    <li><p>Implemented Tomek Links to remove noise from the dataset.</p>

                </ul>
                <h3>Model Training</h3>
                 <ul><li><p>Employed Logistic Regression and.</p>
                    <li><p>Focused on recall and Precision-Recall AUC metrics to evaluate model performance.</p>

                </ul>
        <div/>
        </body>
        </html>

        """
        components.html(workflow_html, height=550, scrolling=True)
    with tab3:
        tech_stack_html = f"""
        <html>
        {common_style_docs}
        <body>
            <div class="container">
                <div class="tech-container">
            <div>
                <div class="tech-item">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" alt="Scikit-learn Logo">
                    <span><strong>ML:</strong> Scikit-learn</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI Logo">
                    <span><strong>API:</strong> FastAPI</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBGxMOnLfFn14dCKzm1lKEKO9ot0fn9yvKQg&s" alt="Docker Logo">
                    <span><strong>Containerization:</strong> Docker</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="https://codelabs.developers.google.com/static/codelabs/cloud-starting-cloudrun-jobs/img/1965fab24c502bd5.png" alt="Google Cloud Run Logo">
                    <span><strong>API Deployment:</strong> Google Cloud Run</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit Logo">
                    <span><strong>Frontend:</strong> Streamlit</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="data:image/png;base64,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" alt="Google Cloud Storage Logo">
                    <span><strong>Cloud Storage:</strong> Google Cloud Storage</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="data:image/png;base64,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" alt="Google BigQuery Logo">
                    <span><strong>Data Access:</strong> Google BigQuery</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/Kaggle_logo.png" alt="Kaggle Logo">
                    <span><strong>Dataset:</strong> Kaggle</span>
                </div>
            </div>
            <div>
                <div class="tech-item">
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOAAAADgCAMAAAAt85rTAAABSlBMVEX///9ChfT7vAXqQzU0qFP7ugA4gPQopUsOoD6VzKGaufgnefM0qFE1pWU/itlChPbqPS78vwDpOzfpOipMgOb0jxn8zVIwffP/++zYuBP729jpNSP//vn7twD80mldlPVNqkrrTUDvQCi3WXtIifT/+/DY5vzMthz+9fTwe3LpLxz0qaTCVGlXfd/v9P74xsLE1/v0+P5lmPX61tPykor97u3sV0voKRP2uLPubGPNTVV8qffwh4CQsviiwvnU4fz3pRH93ZD+8c5woPb7wzX+6rz81YH94aZgq0ZgtnT0oJnwdGroHwDtXlL5zMn0pp6brulmeNLDiJ+zzPrsUC3uYSjwbyLyfh71jwD4uH78ykDtXCr3oRD+8tT97uLxdQD7xlr913f96rF8wYSo17Xg8uXI6NERnVX935vnugZnunua0qlNsWaZu+iBtfloAAALEklEQVR4nO2d6VsaWRaHBVKlATtVSAI2izQJ0CwJuIBCqygq2tGWzIxJnDHNTJuoY5b5/79OsQlVFNQ5d4Pkub9PiY+BenO2e889VTU3JyUlJSUlJSUlJSUlJSUlJSUlJSU1PWUy4Y4ymWlfCUtlyuWNymnWE9kylOuo8yfPWanSDJe/b9byRjGf9eRykYDuGZEeiERyuWq+uFGe9nWSKZwvZTcDERs0C2YiWzptTvtqsSqfVs91O7vZQwY2q6WNaV8zWJnwqb4FhRtA5v4ofRfOGi5mtwI4uL4CufN8eMazTrNUxdrOZMfI5k5l2gwT1MwmaPC6ZvScF6fNYa9MJZejpeuZ0ZOfvWDMVM4iLOi6iiQqM4bY3HEqeEgFqrMUi+WdBGHiHC/dcx6eNldPmXyOOV4HMVKaCT9tnjMMPrMCien7aaaUYBt8ZuWmbsQzLt45kF6daiRusE8uI4S56blpJu/h6Z59bU3NTXdE4BnSz6bips0qt+w5Qrj5RjxfhXpZjdHWqWi+N8LM19HzF39bE8pXyYnl++2ptiuS8I1I9zT4Xr7SXFpcHF9erH/qL55qLpdLXRdlQ8F8z1+8avMZ2i0I4asI5nv5tMfnUr0i+IoJwXx9+3VsKIBPyPLsQb3468tX4823cS6U7/nLv7tMSu7x5QuL5ntl5jOKBV/CLPftkYnvNyufQZjkmEozO0L5LPHXJwzxK4diC+Cg/pmlbvMi3BBaIIbqn1UXnAC5tpdG+ezt10k0aS58dAGoBwIBXU8Y6v7R6ddt44+rk4Y3KeAinupO6TSfLxqq5E9PS2eeyKRm/7j46ym0yp6POIPqkUA2X2xaTjbLzWJlJzHuOGpC/HWdNMnehE0iOD2yVS2OmxXJlDd2/rCbwJgQf30nZb4oDRNkGN1znq04HUk3S9WR1a11fWajJGsnraL59FwVeMhXyerDn/78xVNHPuaZtIjuwUTO4ce05WJ28PlG/Dnzsd4bZrAG1JGnJplKfzTDOf76NmS5JkU2mXRPFd1t7x1TTax/ZhNus+ML4wyoJ4jatO2ttEP9M8nHzoS4RbaeIJw8K55vOdQ/TiYso3a5eoD4MKj8D7j9DDFLpLgUWqUZxvJiAJlV+02EAfUS3bBZLYlAZNSg2RhjwCWzOj/bOqU9rLxAEKpsemxnIwZs87x99/7y2YMu37/7YPw4wGDMLI0gZNKfGWn0vv3w/tm+30axf/5rORWl/sI1OCGT5UxpaJu05Hl3+Wxf8fvdtvK7lat6o0HLuAcnDNHzDXVClz5c/hnzj6PrSlEU//X9Mt131sA+GqJPM/2jlqWlD/sxZSLcA6P7KNii+tJdFQioURf7THeUYunt+/3JprMwxvwnFGZMx4FOqsVp00y5E4E4vC5jTKFAvAhBTUhbKQwPXfJc7ruReF0zBusp0u/dBjopdR4tBYzYI8HrILqPGoTfm4YC0s4mbL37E+ucJsQYabpZBfoo5XLt3/+JUeB1EBWyorG2DcszKlUf/+AvhQ6vg/gXkZ/uJUGA2joFYeOIAV87FI9JFjfAPKMRn8VEV2JM+NqIfoJ0WoCWitA2UTFcXokxwmsTHhHkmkPoklQ9JMg0y0FW5usR4gNxD2pClxpHN7qX2YTfEKEbTVhYB+8qNGwrv8Us/AaEsQMs4QV0zY1ONQ03c762DU+QyRRYKXpuili0tVj7Z58Q6aXQYt+VD+yl0SsufG1CpJd64T7aLvnAPmnKz4mvHYe4ZRvKR10qjDDFtj5YCN2oergGz6NgwmidH16bMIiyIQ7QIHT+SC4JdEixEwwgdN/bV8gxlbb4BWBHygrKgqvgxUxPmlM55FMgSPnm0mhAhyOne4YLbDu+I+Tmt+BDAjpMQTX4Oigyw7SFBpy4xWe8gxjhQ/onGeCko+37meMjAdQOx33YMtcKgY6/jpBloqOxW6cVvnxE/UNcoe+b0N5JD3hmUCL/JAR0hez7+bz2EDR8ZIAu2yMZTpvALh++PlAB+uyq/T3RlXfl9FtE+aUjVSNBtBswaWE9tAN2dBUMBo86f5nwm6T+aWh9PZ7U8JS+0eXMCY5PUfzB43qjlYpGo63GfX3laCwiDZ+hwl7Nux0PIfdNIyZM4WqE4q8fmC47dXDits/C5PE30Fq6Fkctu7W41YTLGD5FObYZF0nV3TZWZMHXVmE1iSn6I8X+I6IIjr3m5euRtRClf5p0iBmCsvooPMUoyv34kxTreZRyxY7P2P6ug41o3RemwAZUghObm61j8y/TjZNYlfbCjyvMu6Y61IDOIXU9+KgYo/gbEpjQ0uiGbgSVFeeDvof/LJbxNyAE++jwcg16lqRcQU4XehUnBvjPwGttF0gYGg5CcK8Q1HrvNgZY1QerCsApKNMwKTAEY3XYNbRbO7z4jEwD3OUnh/7NMQgQfM3Ra4VL/PUEPJLxDf7FMnCd9hF6CQ2efHMF2JHMUPPpAJRjYBmmK9qJ0cmqgUw4NEvaABkwBjag4aQcsAaCTVsOlXoYoML1olECDcwODcuC9oLK9RSJLFqFROGgPxoFNXxjbJeVVAINmGgPh4VRUJVAnj7zFQywv+mF7eaVWQKETHkNVqOgU3mKzhgHgbLMw5YQBshl6Uwq0AwUEvCab23DCXS0PQCE9CsUoqFWXkIC/vAW/P4AecQg0/4YrUA7pgEgqA5+f4X+oQ7+8CsZ4FoUPbDLT6C+zGAtCtxNABsyIgTbTQwAf/j9IHBHT3onGXOlQVOWQ33DA9AElxKcIpNJF6DO6FBPBjbCRXDnAx8BW7/DI13AvuiMbChqsAOYob4otLM9G4mUpLMNPJtA3xbAQ9AbfkxnE8vAA17FPfUVdwF6s4h5GAh8PjjtxsXaNvAE1HKHPcMTXr5CnPCaBkmiiDP6KcZhAX5GH7JMNsOHtRX4IRNrpcH3hBqbQctNoYg5GSXG82xsgi58FHMyuEmnqxPhJX9tdRczv520zt7jbslSPn+6uRWKd7GNmuSyeUrJCWaW6+ff5xe/vf50JwRyLV07XEfh2T5UDjEvqvz8y6NHi4uL8/MLaP33iQ+rUAg/L2r3LG7wxK/y6++PSLX40xOyIWWcbJ8KCJ3Z7thvxgFtZ7aBA4dG/JHzCQIc8zz8FiTNKL9S2E8U4Lj7swCVgpJPDODY27FbjoBU8SfOgmNvsKs7OKnymSb+RAGODqQ/yKH5ROufggDVCU+XaXDmEwE4+UbsCe016vgTA6iOubeup+jYx6woftr4EwKoOT2GLDWmv8bCP0UAOj9Wxr6DyIiPO+CYWyNNTmr3LAsm8ScAUB17f/Iw4eialG79KQ5QBT5527qtYOWfvAHBr2iw1HuGfHwBk+Anpx8MJxpm8ccbEP5Mp7m5jwNCdvHHGdCHepTqQ7Fg6Z98AZGPcPzYzTSM+bgBEjyi8qCdaZTPbPl4AaokL/FJrcTYxh8/wNAh2Zsnrhn7JzdA4gcZ332bn31A8ifEGrp9vLA444DqOt07tG7mmRqRNaAWon678u2nRwwR2QJqI8ecRLr7Ms/MT5kCqvEam7f03d4wSzYMAVVXjd373aJfF+YXWZiRFaCm+rYZvwj05ssiA09lAqipWtzL4XXDN4+/UOcbBoBq6HC3xultyrd3N4sLVHakBNTUUNK7yvFd0Qbj7c3rhYV5IyLbEgaoaQabzxf37hX4vSh6oOjd1y+vX3/71j6mR+qnJypWmisZj68fei+4Ws6G0nDYr4+x+vo/L1a12mpaMJuUlJSUlJSUlJSUlJSUlJSUlJSUlJTUtPR/emjL51h5y8oAAAAASUVORK5CYII=" alt="GCP Logo">
                    <span><strong>Cloud services:</strong> Google Cloud Platform</span>
                </div>
            </div>
        </div>
        </div>
    </body>
    </html>


        """
        components.html(tech_stack_html, height=800, scrolling=True)
    with tab4:
        archi_html= f"""
        <html>
        {common_style_docs}
        <body>

            <div class="container">
            <ul><li><h3>Model Development & Storage</h3>
            <ul>
                <li><strong>Machine Learning Model:</strong><p>A logistic regression model, implemented using scikit-learn, was chosen for fraud detection due to its effectiveness and interpretability.</p></li>
                <li><strong>Data Balancing:</strong><p>To address the class imbalance inherent in credit card fraud datasets, the training data was balanced using the Synthetic Minority Over-sampling Technique (SMOTE). This ensured the model's ability to accurately detect minority (fraudulent) transactions.</p></li>
                <li><strong>Local Training:</strong><p> The logistic regression model was trained locally using the SMOTE-balanced Kaggle Credit Card Fraud Detection dataset.</p></li>
                <li><strong>GCP Storage:</strong><p> The trained, best-performing logistic regression model was serialized and stored in Google Cloud Storage buckets for persistent storage and retrieval.</p></li>
            </ul>

            <li><h3>API Layer</h3>
            <ul>
                <li><strong>Docker Containerization:</strong><p>A REST API (FastAPI) is packaged into a Docker container for consistent deployment.</li>
                <li><strong>Google Cloud Run:</strong><p>  The Docker container is deployed to Google Cloud Run, providing a serverless, scalable environment for the API.</p></li>
                <li><strong>Model Serving:</strong><p>  The API retrieves the trained logistic regression model from Cloud Storage and uses it to perform fraud prediction on incoming transaction data.</p></li>
            </ul>

            <li><h3>Frontend Application</h3>
            <ul>
                <li><strong>Streamlit Interface:</strong><p>A user-friendly web interface is built using Streamlit, enabling users to interact with the application.</p></li>
                <li><strong>API Integration:</strong><p> The Streamlit application connects to the Cloud Run API via HTTP requests to send transaction data and receive fraud prediction results.</p></li>
                <li><strong>Streamlit Cloud Hosting:</strong><p> The Streamlit application is hosted on Streamlit Cloud, providing a platform for easy deployment and accessibility.</p></li>
            </ul>

            <li><h3>Data Flow</h3>
            <ul>
                <li><strong>User Upload:</strong><p> Users upload transaction data (CSV) via the Streamlit interface.</p></li>
                <li><strong>API Request:</strong><p> Streamlit sends the uploaded data to the Cloud Run API.</p></li>
                <li><strong>Model Prediction:</strong><p> The API retrieves the logistic regression model from Cloud Storage, performs fraud prediction, and generates results.</p></li>
                <li><strong>Result Display:</strong><p> The API sends the prediction results back to Streamlit, which displays them to the user.</p></li>
            </ul>
        </div>
        </body>
        </html>
        """
        components.html(archi_html, height=1000, scrolling=True)
    with tab5:
        key_html =f"""
        <head>
        {common_style_docs}
        <body>
        <div class="container">
        <h2>Key Features</h2>
        <ul>
            <li><strong>Fraud Detection:</strong> Accurate detection of fraudulent credit card transactions using a trained machine learning model.</li>
            <br/>
            <li><strong>User-Friendly Interface:</strong> Simple and intuitive web interface for easy data upload and result interpretation.</li>
            <br/>
            <li><strong>Scalable API:</strong> Google Cloud Run deployment ensures the API can handle varying loads.</li>
            <br/>
            <li><strong>Cloud Storage:</strong> Model persistence and retrieval is handled by Google Cloud Storage buckets.</li>
            <br/>
            <li><strong>Data Access:</strong> BigQuery is used for efficient access and querying of transaction data.</li>
            <br/>
            <li><strong>SMOTE Data Balancing:</strong> The model is trained on data balanced using SMOTE to handle class imbalance.</li>

        </ul>
        </div>
    </body>
    </head>
    """
        components.html(key_html, height=500, scrolling=True)

    with tab6:
        fut_html =f"""
        <head>
        {common_style_docs}
        <body>
        <div class="container">
        <h2>Future Improvements</h2>
                <ul>
            <li><strong>Real-time Processing:</strong> Implement real-time fraud detection capabilities for immediate alerts.</li>
            <br/>
            <li><strong>Enhanced Visualization:</strong> Add more detailed visualizations of transaction data and fraud patterns for better analysis.</li>
            <br/>
            <li><strong>Integration:</strong> Seamlessly integrate with bank security architectures for automated alerts and responses.</li>
            <br/>
            <li><strong>Model Retraining:</strong> Implement a system for automated model retraining on new data to maintain accuracy.</li>
            <br/>
            <li><strong>Expanded Feature Set:</strong> Add features like user authentication, detailed transaction reports, and customizable alert thresholds.</li>
            <br/>
            <li><strong>Explainable AI:</strong> Incorporate techniques to provide explanations for fraud predictions, improving transparency and trust.</li>
            </ul>
        </div>
        </body>
        </html>

 """
        components.html(fut_html, height=500, scrolling=True)

elif page == "User Manual":
    usage_manual_html = """
    <style>
        .top-container {
            background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
            padding: 10px;
            border-radius: 12px;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
            width: 80%;
            margin: 20px auto;
            text-align: center;
            font-family: 'Open Sans', sans-serif;
        }
        .bottom-container {
            background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
            padding: 10px;
            border-radius: 12px;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
            width: 80%;
            margin: 20px auto;
            text-align: center;
            font-family: 'Open Sans', sans-serif;
        }
        .manual-container {
            background: linear-gradient(135deg, #e3f2fd, #f8f9fa); /* Light gradient */
            padding: 10px;
            border-radius: 12px;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
            width: 80%;
            margin:20px auto;
            text-align: center;
            font-family: 'Open Sans', sans-serif;

        }
        .manual-title {
            font-size: 24px;
            font-weight: bold;
            color: #007bff; /* Blue title */
            margin-bottom: 20px;
        }
        .manual-step {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 15px;
        }
        .manual-text {
            font-size: 16px;
            color: #555;
        }
        .other-text-title {
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-top: 10px;
        }
        .other-text {
            font-size: 14px;
            color: #333;
            margin-top: 10px;
            text-align: left;
        }
    </style>
        <div class="top-container">
            <p class="other-text-title">🎯 Intended Audience</p>
            <p class="other-text">This web app is intended for bank employees and security personnel who need to analyze transaction data for potential fraud. It provides a user-friendly interface to upload transaction files and quickly identify fraudulent activities.</p>
        </div>

        <div class="manual-container">
            <p class="manual-title">📖 How to Use This Web App</p>

            <p class="manual-step">1️⃣ Prepare Your Data</p>
            <p class="manual-text">Ensure your transaction file is already transformed into CSV format and has 30 columns.</p>

            <p class="manual-step">2️⃣ Upload the File</p>
            <p class="manual-text">Go to the Dashboard and use the file uploader to select your transaction file.</p>

            <p class="manual-step">3️⃣ Wait for the Fraud Detection</p>
            <p class="manual-text">The system will analyze transactions and detect fraudulent activities.</p>

            <p class="manual-step">4️⃣ Interpreting Results</p>
            <p class="manual-text">
                ✅ <span style="color: green;">No fraud detected:</span> You'll see a green message. <br>
                ❌ <span style="color: red;">Fraud detected:</span> You'll see a red message with fraud row numbers.
            </p>
        </div>

        <div class="bottom-container">
            <p class="other-text-title">⚙️ Ideal Scenario</p>
            <p class="other-text">In an ideal scenario, this app and its underlying fraud detection model would be seamlessly integrated into a bank's security architecture. This would enable real-time monitoring of transactions and automatic notifications to responsible personnel upon the detection of fraudulent activities, ensuring swift and effective response.</p>
        </div>

"""

# Render the HTML correctly
    components.html(usage_manual_html, height=800)

elif page == "Team":
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
                        <p>Transitioning into AI and Data Science, combining 10+ years of business experience in technical equipment distribution, sales, negotiations, tenders, project management, and strategic planning.</p>
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
                    <p>I am a data scientist with a PhD in physics, passionate about applying machine learning and statistical analysis to solve complex real-world problems. With a strong analytical background and expertise in data preprocessing, model development, and optimization, I focus on building efficient and interpretable AI solutions. Currently, I am working on credit card fraud detection, leveraging advanced machine learning techniques to enhance security in financial transactions.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Render the HTML inside Streamlit
    components.html(team_html, height=1500)

    def encode_video(video_path):
        with open(video_path, "rb") as vid_file:
            return base64.b64encode(vid_file.read()).decode()


    video_path = os.path.abspath("assets/memories_compressed.mp4")
    st.video(video_path)

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
                .st-emotion-cache-wq5ihp {
                font-family: "Open Sans", sans-serif;
                font-size: 1.875rem;
                font-weight: bold;
                color: white;
    }
            }

    /* Adjust the file drop area */
    div[data-testid="stFileDropzone"] {
        min-height: 200px !important; /* Adjust the height */
        padding: 20px !important;
        align: left;
    }
     div[data-baseweb="tab-list"] button {
         .st-emotion-cache-wq5ihp {
                font-family: "Open Sans", sans-serif;
                font-size: 1.5rem;
                font-weight: bold;
                color: white;
            }

           }

    </style>

    """,
    unsafe_allow_html=True,
)
