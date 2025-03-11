import streamlit as st
import pandas as pd
import base64
from PIL import Image
from io import BytesIO, StringIO

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

# 2. Define the navigation_bar function
def navigation_bar():
    col1, col2, col3, col4 = st.columns([8, 8, 8, 1])

    with col1:
        if st.markdown('<button class="button-blue">Home</button>', unsafe_allow_html=True):
            st.session_state.page = "main"

    with col2:
        if st.markdown('<button class="button-blue">Dashboard</button>', unsafe_allow_html=True):
            st.session_state.page = "dashboard"

    with col3:
        if st.markdown('<button class="button-blue">🔔</button>', unsafe_allow_html=True):
            st.write("Nota bene: Notifications will appear here.")

    with col4:
        profile_image_path = "profile.png"
        try:
            profile_image = Image.open(profile_image_path)
            if st.markdown(f'<button class="button-blue"><img src="data:image/png;base64,{image_to_base64(profile_image)}" width="50"></button>', unsafe_allow_html=True):
                st.session_state.page = "profile"
        except FileNotFoundError:
            if st.markdown('<button class="button-blue">👤</button>', unsafe_allow_html=True):
                st.session_state.page = "profile"

# 3. Define the main function
def main():
    if "page" not in st.session_state:
        st.session_state.page = "main"

    navigation_bar()

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if st.session_state.page == "main":
        st.write("Main Page Content")

        # File Upload Section
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            #st.write("Uploaded bytes:", bytes_data)

            # To read file as string:
            string_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
            #st.write("Uploaded string:", string_data)

            # Can be used wherever a "file-like" object is accepted:
            dataframe = pd.read_csv(uploaded_file)
            st.write("Uploaded DataFrame:", dataframe)

    elif st.session_state.page == "dashboard":
        st.write("Dashboard Content")
    elif st.session_state.page == "profile":
        st.write("Profile Content")

    st.markdown('</div>', unsafe_allow_html=True)

# 4. Convert Image to Base64 (helper function)
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

if __name__ == "__main__":
    main()

st.write("Upload your document here")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write("Uploaded DataFrame:", dataframe)

#st.write("Navigation bar")
#st.write("Upload the file here")
