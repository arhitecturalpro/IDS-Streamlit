import streamlit as st
from streamlit_option_menu import option_menu

def show_sidebar():
    """Render the sidebar with the navigation menu."""
    # Add custom CSS to move the logo to the very top of the sidebar
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            padding-top: 0 !important;  /* Remove existing padding */
        }
        .sidebar .sidebar-content img {
            margin-top: -20px; /* Adjust the value to move the logo higher */
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Sidebar block
    with st.sidebar:
        # Add the logo at the top of the sidebar
        st.image("images/logo.png", width=300)  # Replace with your logo path and adjust the width as needed
        
        selected = option_menu(
            menu_title="IDS",  # Sidebar title
            options=["Home", "View Mode", "Settings", "Detected Human"],  # Menu options
            icons=["house", "eye", "gear", "person-check"],  # Corresponding icons
            menu_icon="cast",  # Icon for the sidebar
            default_index=0,  # Default selected option
            orientation="vertical",  # Sidebar orientation
        )
    return selected
