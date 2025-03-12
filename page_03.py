import streamlit as st
from PIL import Image

# Define a key for session state storage
PROFILE_PIC_KEY = "profile_pic"

def show_page():
    st.write("### Profile Page")

    # Load existing profile picture from session state
    if PROFILE_PIC_KEY in st.session_state:
        st.image(st.session_state[PROFILE_PIC_KEY], caption="Your Profile Picture")

        # Remove profile picture button
        if st.button("Remove Profile Picture"):
            del st.session_state[PROFILE_PIC_KEY]
            st.experimental_rerun()  # Refresh the page after removal
    else:
        # File uploader for new profile picture
        uploaded_image = st.file_uploader("Upload your profile picture", type=["png", "jpg", "jpeg"])

        if uploaded_image:
            image = Image.open(uploaded_image)

            # Keep aspect ratio, max size 150x150 pixels
            image.thumbnail((150, 150))

            # Save in session state
            st.session_state[PROFILE_PIC_KEY] = image
            st.experimental_rerun()  # Refresh the page to show uploaded image
