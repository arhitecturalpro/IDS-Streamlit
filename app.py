import streamlit as st
from navbar import show_sidebar  
from login import login
from signup import sign_up
from home import home
from detected import detected  # Assuming detected() handles image display
from viewmode import view_mode
from setting import settings  # Import settings function from settings.py

def add_background_image(image_url):
    """Set a background image for the app."""
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Add the background image
    add_background_image("images/wallpaper.jpg")  # Replace with the correct path to your image

    st.title("")  # Title placeholder

    # Show the navbar and get the selected page
    page = show_sidebar()

    # Handle the page content based on the selected option
    if page == "Login":
        login()
    elif page == "Sign Up":
        sign_up()
    elif page == "View Mode":
        view_mode()  # Trigger the camera view mode functionality
    elif page == "Home":
        home()  # Call the home function when "Home" is selected in the sidebar
    elif page == "Detected Human":
        detected()  # Display the detected images when the "Detected" page is selected
    elif page == "Settings":
        settings()  # Call the settings function when "Settings" is selected in the sidebar
    else:
        st.write("Welcome to the Home Page!")

if __name__ == "__main__":
    main()
