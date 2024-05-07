import streamlit as st
import numpy as np
from PIL import Image, ImageEnhance
import io
import pandas as pd
import cv2
from sklearn.cluster import KMeans
from plotly import graph_objects as go

#make sure all packages are pip installed cv2, PIL and Kmeans are important

# we want to first check image properties and adjust them as required
def adjust_image(image, saturation, hue, temperature, tint, vibrance):
    # image to numpy array
    img_array = np.array(image)
    
    # RGB image to HSL color space
    img_hsl = Image.fromarray(img_array).convert("HSV")
    
    # saturation
    enhancer = ImageEnhance.Color(img_hsl)
    img_hsl = enhancer.enhance(saturation)
    
    # hue
    enhancer = ImageEnhance.Color(img_hsl)
    img_hsl = enhancer.enhance(hue)
    
    # back to RGB
    img_rgb = img_hsl.convert("RGB")
    
    #  temperature 
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(temperature)
    
    # tint
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(tint)
    
    #   vibrance
    enhancer = ImageEnhance.Color(img_rgb)
    img_rgb = enhancer.enhance(vibrance)
    
    return img_rgb

# download image
def download_image(image, filename="image.jpg"):
    # PIL image to bytes so that fomatting is good
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    # download file option
    st.download_button(label="Download Image", data=img_bytes, file_name=filename)

# recognize color
def recognize_color(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(csv)):
        try:
            d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        except ValueError:
            # adding the option to skip if any of the RGB values cannot be converted to integers
            continue
        if d <= minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name

# compute dominant colors
def compute_dominant_colors(image, k=10):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_flat = img.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img_flat)
    colors = kmeans.cluster_centers_.astype(int)
    return colors

# cache data so that app runs smoothly!
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df


index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('data/colors.csv', names=index, header=None)

# images to be displayed
thumbnail_images = {
    "Dog": "images/dog.jpg",
    "Food": "images/food.jpg",
    "Toucan": "images/toucan.jpg",
    "Toy": "images/toy.jpg",
    "Bridge": "images/bridge.jpg"
}

st.title("📸 Mini Lightroom App")

st.write("🎞 A mini Lightroom app is like having a pocket-sized photo studio in your hands! It lets you tweak and enhance your photos with powerful editing tools, from adjusting brightness and contrast to fine-tuning colors and adding artistic effects.")

st.write("📕 Saturation: Controls the intensity or vividness of colors in an image.")
st.write("📔 Hue: Represents the color's position on the color wheel, determining its shade or tint.")
st.write("📘 Temperature: Adjusts the warmth or coolness of colors in an image, mimicking the effect of different lighting conditions.")
st.write("📗 Tint: Adds a subtle color cast to an image, often used to create artistic effects or correct color balance.")
st.write("📙 Vibrance: Enhances the intensity of muted colors without affecting skin tones, making them appear more vibrant and lively.")


selected_image = st.selectbox("Select an image", list(thumbnail_images.keys()))

# selected image
file_path = thumbnail_images[selected_image]
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key=selected_image)

if uploaded_file is not None:
    
    file_bytes = uploaded_file.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
else:
    
    img = cv2.imread(file_path)

# resize 
img_resized = cv2.resize(img, (500, int(img.shape[0] * (500 / img.shape[1]))))

# dominant color calculation
colors = compute_dominant_colors(img_resized, k=10)

#colors to hexadecimal and get color names 
colors_hex = ['#%02x%02x%02x' % (color[0], color[1], color[2]) for color in colors]
color_names = [recognize_color(color[0], color[1], color[2]) for color in colors]

#proportions of colors
proportions = np.random.rand(len(colors))

# sorting colors and proportions by proportions in descending order
sorted_indices = np.argsort(proportions)[::-1]
sorted_color_names = [color_names[i] for i in sorted_indices]
sorted_colors_hex = [colors_hex[i] for i in sorted_indices]
sorted_proportions = [proportions[i] for i in sorted_indices]

#Plotly bar chart for color composition
bar = go.Figure(data=[go.Bar(x=sorted_color_names, y=sorted_proportions,
                             marker=dict(color=sorted_colors_hex))])

bar.update_layout(title='Dominant Color Composition', xaxis_title='Color',
                  yaxis_title='Proportion', showlegend=False,
                  width=300, height=400)

original_properties = {
    "saturation": 1.0,
    "hue": 1.0,
    "temperature": 1.0,
    "tint": 1.0,
    "vibrance": 1.0
}


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

# have to make sure in bytes so that there are no errors. 
def download_image(image, filename="image.jpg"):
    
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes.getvalue(), file_name=filename)

# Download button
#download_image(Image.fromarray(adjusted_image))