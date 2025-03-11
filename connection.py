import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from bson import Binary
from io import BytesIO
from PIL import Image

# Function to connect to MongoDB
def connect_to_mongodb():
    try:
        uri = "mongodb+srv://openmyca123:openmyca123@idscluster.wku0w.mongodb.net/?retryWrites=true&w=majority&appName=IDSCluster"
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)  # Timeout after 5 seconds
        db = client["human_detections"]  # Replace with your actual database name
        collection = db["detections"]  # Replace with your collection name
        return collection
    except ServerSelectionTimeoutError as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None

# Function to fetch the image from MongoDB
def fetch_image_from_mongodb(collection):
    # Fetch the most recent image (or a specific query depending on your use case)
    document = collection.find_one({}, sort=[("timestamp", -1)])  # Sort by timestamp (most recent first)
    if document and "image" in document:
        img_binary = document["image"]
        # Convert binary data back to image
        img = Image.open(BytesIO(img_binary))
        return img
    else:
        return None

# Streamlit UI
def main():
    st.title("Human Detection Images")
    
    # Connect to MongoDB
    collection = connect_to_mongodb()
    if collection is not None:
        # Fetch the image from MongoDB
        img = fetch_image_from_mongodb(collection)
        
        if img:
            # Display the image in Streamlit
            st.image(img, caption="Captured Human Detection", use_column_width=True)
        else:
            st.write("No image found in the database.")
    else:
        st.write("Failed to connect to MongoDB.")

if __name__ == "__main__":
    main()
