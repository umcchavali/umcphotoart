import streamlit as st
from PIL import Image, ImageOps
from PIL import ImageEnhance

#from Pillow import ImageEnhance

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

# Function to simulate vision of other animals
def simulate_animal_vision(image, animal_type):
    # Convert image to grayscale
    img_gray = ImageOps.grayscale(image)
    
    # Simulate vision based on the selected animal type
    if animal_type == "Dog":
        # Simulate dog vision (blue-yellow colorblindness)
        img_animal = ImageOps.colorize(img_gray, black="#8B8682", white="#FFFF00")
    elif animal_type == "Cat":
        # Simulate cat vision (similar to grayscale)
        img_animal = img_gray
    elif animal_type == "Bird":
        # Simulate bird vision (enhanced UV perception)
        img_animal = ImageEnhance.Brightness(img_gray).enhance(1.5)
    else:
        # Default to grayscale
        img_animal = img_gray
    
    return img_animal

# Function to download image
def download_image(image, filename="image.jpg"):
    # Convert PIL image to bytes
    img_bytes = image.tobytes()
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes, file_name=filename)

# Load image
st.title("Vision Simulator")
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Define simulation options
simulation_options = {
    "Normal Vision": "No visual impairment. Normal human vision.",
    "Deuteranopia": "Green-blindness. Difficulty in distinguishing between red and green colors.",
    "Protanopia": "Red-blindness. Difficulty in distinguishing between red and green colors.",
    "Tritanopia": "Blue-blindness. Difficulty in distinguishing between blue and yellow colors.",
    "Dog": "Simulated vision of a dog. Blue-yellow colorblindness.",
    "Cat": "Simulated vision of a cat. Similar to grayscale vision.",
    "Bird": "Simulated vision of a bird. Enhanced UV perception."
}

# Display predefined images for selection
st.subheader("Select a predefined image:")
image_options = {
    "Dog": "images/dog.jpg",
    "Food": "images/food.jpg",
    "Toucan": "images/toucan.jpg",
    "Toy": "images/toy.jpg",
    "Bridge": "images/bridge.jpg"
}
selected_image_option = st.radio("Choose an image option", list(image_options.keys()))
if selected_image_option:
    image_path = image_options[selected_image_option]
    image = Image.open(image_path)
    st.image(image, caption=selected_image_option, use_column_width=True)

if uploaded_image is not None:
    # Read image
    image = Image.open(uploaded_image)

# Select vision type
vision_type = st.selectbox("Select vision type:", list(simulation_options.keys()))

# Display description for selected vision type
st.write(simulation_options[vision_type])

# Simulate vision
if uploaded_image is not None or selected_image_option:
    if vision_type == "Normal Vision":
        st.image(image, caption="Original Image", use_column_width=True)
        download_image(image)
    else:
        if vision_type in ["Deuteranopia", "Protanopia", "Tritanopia"]:
            simulated_image = simulate_color_blindness(image, vision_type)
        else:
            simulated_image = simulate_animal_vision(image, vision_type)
        st.image(simulated_image, caption=f"Simulated {vision_type} Vision", use_column_width=True)
        download_image(simulated_image)
