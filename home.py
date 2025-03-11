import streamlit as st

def home():
    # URL of the header image
    header_image_url = "https://www.vmprotect.net/wp-content/uploads/2023/06/pexels-scott-webb-430208-2000x1125.jpg"

    # Add custom CSS for styling with adjustments
    st.markdown(
        f"""
        <style>
            /* App Styling */
            .stApp {{
                background: linear-gradient(180deg, #000000, #2C2C2C);
                font-family: 'Poppins', sans-serif;
            }}
            /* Header Styling */
            .header {{
                position: relative;
                text-align: center;
                padding: 0;
                margin: 0 auto;
                max-width: 900px;
                border-radius: 15px;
                box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
                overflow: hidden;
                margin-top: -0.1rem; /* Moves the header image higher */
            }}
            .header img {{
                width: 100%;
                height: auto;
                display: block;
                animation: fadeIn 2s ease-out;
            }}
            .header-text {{
                position: absolute;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
            }}
            .header-text h1 {{
                font-size: 3rem;
                margin: 0;
                font-weight: bold;
                color: #00FF7F;
                animation: fadeInUp 1.5s ease-out;
            }}
            .header-text p {{
                font-size: 1.3rem;
                margin: 0;
                color: #dcdcdc;
                animation: fadeInUp 1.5s ease-out 0.5s;
            }}
            /* Features Section Styling */
            .features {{
                display: flex;
                justify-content: space-between;
                margin: 0 auto;
                padding: 1.5rem 1rem;
                max-width: 900px;
                gap: 1rem;
                border-radius: 15px;
                background: linear-gradient(135deg, #32CD32, #87CEEB);
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                margin-top: -9rem; /* Ensures features section aligns properly */
                animation: slideUp 1.5s ease-out;
            }}
            .card {{
                flex: 1;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                padding: 1rem;
                text-align: center;
                color: #333;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                transform: translateY(50px);
                opacity: 0;
                animation: fadeInUpCard 1s ease-out forwards;
            }}
            .card i {{
                font-size: 3rem;
                color: #00FF7F;
                margin-bottom: 1rem;
            }}
            .card h3 {{
                font-size: 1.25rem;
                margin-bottom: 1rem;
                color: #00FF7F;
            }}
            .card p {{
                font-size: 1rem;
                color: #555;
            }}
            /* YouTube Section Styling */
            .video-container {{
                text-align: center;
                margin: 2rem auto;
                padding: 1rem;
                border-radius: 15px;
                background: linear-gradient(135deg, #32CD32, #87CEEB);
                max-width: 980px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }}
            iframe {{
                border-radius: 10px;
            }}
            /* Footer Styling */
            .footer {{
                text-align: center;
                padding: 1.5rem;
                color: white;
                margin-top: 1rem;
                font-size: 0.9rem;
                background: linear-gradient(135deg, #32CD32, #87CEEB);
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                font-weight: bold;
                letter-spacing: 0.5px;
                padding-left: 2rem;
                padding-right: 2rem;
            }}
            .footer a {{
                color: #00FF7F;
                text-decoration: none;
            }}
            .footer a:hover {{
                text-decoration: underline;
            }}
            /* Keyframes for Animations */
            @keyframes fadeIn {{
                0% {{ opacity: 0; }}
                100% {{ opacity: 1; }}
            }}
            @keyframes fadeInUp {{
                0% {{ opacity: 0; transform: translateY(30px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes slideUp {{
                0% {{ opacity: 0; transform: translateY(30px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes fadeInUpCard {{
                0% {{ opacity: 0; transform: translateY(50px); }}
                100% {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    # Header Section with Image and Text Overlay
    st.markdown(
        f"""
        <div class="header">
            <img src="{header_image_url}" alt="Header Image">
            <div class="header-text">
                <h1>Welcome to IDS!</h1>
                <p>Real-time Intrusion Detection using YOLOv7</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features Section with Icons
    st.markdown(
        """
        <div class="features">
            <div class="card">
                <i class="fas fa-broadcast-tower"></i>
                <h3>Real-Time Detection</h3>
                <p>Leverage YOLOv7 for fast and accurate human detection in live video streams.</p>
            </div>
            <div class="card">
                <i class="fas fa-bell"></i>
                <h3>Alarm Notification</h3>
                <p>Get instant alarms when a human is detected to enhance security.</p>
            </div>
            <div class="card">
                <i class="fas fa-camera-retro"></i>
                <h3>Automatic Screenshots</h3>
                <p>Capture and save images automatically upon detection, with timestamps.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # YouTube Section
    youtube_url = "https://www.youtube.com/embed/dsnxQguXBmk?autoplay=1&mute=1&loop=1&playlist=dsnxQguXBmk"
    st.markdown(
        f"""
        <div class="video-container">
            <iframe width="100%" height="400" src="{youtube_url}" 
            frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Footer Section
    st.markdown(
        """
        <div class="footer">
            &copy; 2025 IDS. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Call home function to display
home()
