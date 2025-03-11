import streamlit as st
from PIL import Image
import os
from io import BytesIO
import base64

def detected():
    """Streamlit page to display detected images in a grid layout."""

    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .stApp { background: linear-gradient(180deg, #000000, #2C2C2C); font-family: 'Poppins', sans-serif; }
            .title { text-align: center; color: #00FF7F; font-weight: bold; font-size: 2rem; margin-top: 1rem; margin-bottom: 0.5rem; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); }
            .subtitle { text-align: center; color: #87CEEB; font-size: 1.2rem; margin-bottom: 1.5rem; }
            .folder-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 2rem; padding: 1rem; }
            .folder {
                width: 350px; height: 160px; background: linear-gradient(to bottom, #FFD700, #DAA520); 
                border-radius: 15px; display: flex; flex-direction: column; justify-content: center; align-items: center;
                box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.3); transition: transform 0.3s ease-in-out;
                cursor: pointer; font-size: 1.3rem; font-weight: bold; color: #333;
                border-top-left-radius: 30px; position: relative; padding-top: 15px;
            }
            .folder:hover { transform: scale(1.08); }
            .folder:before {
                content: ''; position: absolute; top: -12px; left: 15px;
                width: 100px; height: 20px; background: #FFD700; border-top-left-radius: 10px; 
                border-top-right-radius: 10px;
            }
            .no-images { text-align: center; color: #FF6347; font-size: 1.2rem; margin-top: 2rem; }
            .folder-not-found { text-align: center; color: #FF4500; font-size: 1.2rem; margin-top: 2rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="title">Detected Humans</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Click a folder to view detected images for that date:</div>', unsafe_allow_html=True)

    folder_path = r"C:\Users\USER\Documents\thesis-ids\IDS\detected_human"

    if os.path.exists(folder_path):
        date_folders = sorted(os.listdir(folder_path), reverse=True)

        if date_folders:
            st.markdown('<div class="folder-container">', unsafe_allow_html=True)

            for date_folder in date_folders:
                full_path = os.path.join(folder_path, date_folder)
                if os.path.isdir(full_path):
                    clicked = st.toggle(f"📂 {date_folder}", key=date_folder)
                    if clicked:
                        image_files = [f for f in os.listdir(full_path) if f.endswith((".jpg", ".png"))]
                        if image_files:
                            num_columns = 4  # Adjust number of images per row
                            cols = st.columns(num_columns)

                            for idx, image_file in enumerate(image_files):
                                img_path = os.path.join(full_path, image_file)
                                image = Image.open(img_path)
                                
                                # Display images in grid columns
                                with cols[idx % num_columns]:
                                    st.image(image, use_container_width=True)
                        else:
                            st.markdown('<div class="no-images">No images in this folder.</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-images">No detected images yet.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="folder-not-found">The "detected_human" folder does not exist.</div>', unsafe_allow_html=True)

