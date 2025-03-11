import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# 1. Define CSS styles
st.markdown(
    """
    <style>
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

    if st.session_state.page == "main":
        st.write("Main Page Content")
    elif st.session_state.page == "dashboard":
        st.write("Dashboard Content")
    elif st.session_state.page == "profile":
        st.write("Profile Content")

# 4. Convert Image to Base64 (helper function)
import base64
def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

from io import BytesIO

if __name__ == "__main__":
    main()

st.write("Navigation bar")
st.write("Upload the file here")
