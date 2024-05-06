import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import pandas as pd
import cv2
from sklearn.cluster import KMeans
from PIL import ImageOps

# Function to simulate color blindness
def simulate_color_blindness(image, blindness_type):
    # Convert image to grayscale
    img_gray = ImageOps.grayscale(image)
    
    # Simulate color blindness based on the selected type
    if blindness_type == "Deuteranopia":
        # Simulate deuteranopia (green-blind)
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#F0E68C")
    elif blindness_type == "Protanopia":
        # Simulate protanopia (red-blind)
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#DAA520")
    elif blindness_type == "Tritanopia":
        # Simulate tritanopia (blue-blind)
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#FF69B4")
    else:
        # Default to grayscale
        img_blind = img_gray
    
    return img_blind

# Function to download image
def download_image(image, filename="image.jpg"):
    # Convert PIL image to bytes
    img_bytes = image.tobytes()
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes, file_name=filename)

# Load image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Read image
    image = Image.open(uploaded_image)
    
    # Define color blindness types and descriptions
    blindness_types = {
        "Normal Vision": "No color blindness. Normal vision with full color perception.",
        "Deuteranopia": "Green-blindness. Difficulty in distinguishing between red and green colors.",
        "Protanopia": "Red-blindness. Difficulty in distinguishing between red and green colors.",
        "Tritanopia": "Blue-blindness. Difficulty in distinguishing between blue and yellow colors."
    }
    
    # Select color blindness type
    blindness_type = st.selectbox("Select color blindness type:", list(blindness_types.keys()))
    
    # Display description for selected color blindness type
    st.write(blindness_types[blindness_type])
    
    # Simulate color blindness
    if blindness_type != "Normal Vision":
        simulated_image = simulate_color_blindness(image, blindness_type)
        st.image(simulated_image, caption="Simulated Color Blindness", use_column_width=True)
        download_image(simulated_image)
    else:
        st.image(image, caption="Original Image", use_column_width=True)
        download_image(image)
