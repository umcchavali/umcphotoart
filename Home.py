import streamlit as st
from PIL import Image, ImageEnhance
import base64

# Load the image
background_image = Image.open('images/rose.jpg')

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Convert the image to bytes
image_bytes = background_image.tobytes()

# Encode the image bytes to base64
encoded_image = base64.b64encode(image_bytes).decode()

# Set the background image
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url('data:image/jpeg;base64,{encoded_image}') no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to UMCPhotoart! 🎨")

st.write("Hey there, welcome to UMCPhotoart! Ready to dive into a whole new world where art, photography, tech, and innovative ideas collide? Here, we're all about exploring creativity in every pixel and embracing the magic of visual storytelling.")

st.write(
    "Whether you're a seasoned pro or just getting started, there's something here for everyone! Get ready to unleash your inner artist with features like our mini lightroom app 📸, perfect for tweaking those pics until they're Instagram-ready. Plus, we've got a vision simulator 👓 that lets you see the world through different eyes – literally!"
)

st.write(
    "And if you're ever stuck on finding the perfect color palette, don't sweat it. Our color palette finder 🎨 has got your back. Oh, and speaking of Instagram, be sure to check out our page @umc.photoart for some extra inspiration and behind-the-scenes fun. Let's create something awesome together!"
)


st.markdown(
    '<a href="https://www.instagram.com/umc.photoart/" target="_blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/1024px-Instagram_icon.png" width="30"></a>'
    '<a href="https://www.instagram.com/umc.photoart/" target="_blank">@umc.photoart</a>',
    unsafe_allow_html=True
)

# Display your custom logo
#st.image("https://via.placeholder.com/100", caption="Your Custom Logo", width=100)
st.markdown(
    '<a href="https://www.etsy.com/shop/UMCPhotoart" target="_blank"><img src="images/etsy.jpg" width="30"></a>'
    '<a href="https://www.etsy.com/shop/UMCPhotoart" target="_blank">UMCPhotoart Etsy Shop</a>',
    unsafe_allow_html=True
)