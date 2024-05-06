import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import io
import pandas as pd
import cv2
from sklearn.cluster import KMeans
from plotly import graph_objects as go

# Function to adjust image properties
def adjust_image(image, saturation, hue, temperature, tint, vibrance):
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Convert RGB image to HSL color space
    img_hsl = Image.fromarray(img_array).convert("HSV")
    
    # Adjust saturation
    enhancer = ImageEnhance.Color(img_hsl)
    img_hsl = enhancer.enhance(saturation)
    
    # Adjust hue
    enhancer = ImageEnhance.Color(img_hsl)
    img_hsl = enhancer.enhance(hue)
    
    # Convert back to RGB
    img_rgb = img_hsl.convert("RGB")
    
    # Adjust temperature (color balance)
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(temperature)
    
    # Adjust tint
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(tint)
    
    # Adjust vibrance
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(vibrance)
    
    return img_rgb

# Function to download image
def download_image(image, filename="image.jpg"):
    # Convert PIL image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes, file_name=filename)

# Function to recognize color
def recognize_color(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(csv)):
        try:
            d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        except ValueError:
            # Skip if any of the RGB values cannot be converted to integers
            continue
        if d <= minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name

# Function to compute dominant colors
def compute_dominant_colors(image, k=10):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_flat = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img_flat)
    colors = kmeans.cluster_centers_.astype(int)
    return colors

# Load color data from CSV file
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load color data
index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('data/colors.csv', names=index, header=None)

# Thumbnail images
thumbnail_images = {
    "Image 1": "data/Untitled_Artwork.jpg",
    "Image 2": "data/Untitled_Artwork.jpg",
    "Image 3": "data/Untitled_Artwork.jpg",
    "Image 4": "data/Untitled_Artwork.jpg",
    "Image 5": "data/522416403-removebg-preview.png"
}

st.title("Mini Lightroom App")

# Select image
selected_image = st.selectbox("Select an image", list(thumbnail_images.keys()))

# Read selected image
file_path = thumbnail_images[selected_image]
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key=selected_image)

if uploaded_file is not None:
    # Read image
    file_bytes = uploaded_file.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
else:
    # Load selected thumbnail image
    img = cv2.imread(file_path)

# Resize image to a fixed size
img_resized = cv2.resize(img, (500, int(img.shape[0] * (500 / img.shape[1]))))

# Compute dominant colors
colors = compute_dominant_colors(img_resized, k=10)

# Convert colors to hexadecimal and get color names
colors_hex = ['#%02x%02x%02x' % (color[0], color[1], color[2]) for color in colors]
color_names = [recognize_color(color[0], color[1], color[2]) for color in colors]

# Calculate proportions of colors
proportions = np.random.rand(len(colors))

# Sort colors and proportions by proportions in descending order
sorted_indices = np.argsort(proportions)[::-1]
sorted_color_names = [color_names[i] for i in sorted_indices]
sorted_colors_hex = [colors_hex[i] for i in sorted_indices]
sorted_proportions = [proportions[i] for i in sorted_indices]

# Create Plotly bar chart for color composition
bar = go.Figure(data=[go.Bar(x=sorted_color_names, y=sorted_proportions,
                             marker=dict(color=sorted_colors_hex))])

# Customize layout
bar.update_layout(title='Dominant Color Composition', xaxis_title='Color',
                  yaxis_title='Proportion', showlegend=False,
                  width=300, height=400)

# Store original image properties
original_properties = {
    "saturation": 1.0,
    "hue": 1.0,
    "temperature": 1.0,
    "tint": 1.0,
    "vibrance": 1.0
}

# Display original image and bar plot
st.subheader("Original Image and Dominant Color Composition")
col1, col2 = st.columns([2, 1])
with col1:
    st.image(img_resized, channels="BGR", caption="Uploaded Image")
    st.subheader("Adjust Image Properties")
    saturation = st.slider("Saturation", 0.0, 2.0, original_properties["saturation"])
    hue = st.slider("Hue", 0.0, 2.0, original_properties["hue"])
    temperature = st.slider("Temperature", 0.0, 2.0, original_properties["temperature"])
    tint = st.slider("Tint", 0.0, 2.0, original_properties["tint"])
    vibrance = st.slider("Vibrance", 0.0, 2.0, original_properties["vibrance"])
    if st.button("Reset Controls"):
        saturation = original_properties["saturation"]
        hue = original_properties["hue"]
        temperature = original_properties["temperature"]
        tint = original_properties["tint"]
        vibrance = original_properties["vibrance"]
with col2:
    st.plotly_chart(bar)
    adjusted_image = adjust_image(img_resized, saturation, hue, temperature, tint, vibrance)
    st.subheader("Adjusted Image")
    st.image(adjusted_image, caption="Adjusted Image", width=500)

# Download button
#download_image(Image.fromarray(adjusted_image))

# Function to download image
def download_image(image, filename="image.jpg"):
    # Convert PIL image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes.getvalue(), file_name=filename)

# Download button
#download_image(Image.fromarray(adjusted_image))