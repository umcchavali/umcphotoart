import streamlit as st
from PIL import Image, ImageOps
from PIL import ImageEnhance

#from Pillow import ImageEnhance - make sure pillow is pip installed

#here create different type of color blindness functions

def simulate_color_blindness(image, blindness_type):
    # convert image to grayscale
    img_gray = ImageOps.grayscale(image)
    
    
    if blindness_type == "Deuteranopia": #green blind
        
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#F0E68C")
    elif blindness_type == "Protanopia": #red blind
       
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#DAA520")
    elif blindness_type == "Tritanopia": #blue blind
        
        img_blind = ImageOps.colorize(img_gray, black="#8B8682", white="#FF69B4")
    else:
       
        img_blind = img_gray
    
    return img_blind

# make a function for animals as well
def simulate_animal_vision(image, animal_type):
    
    img_gray = ImageOps.grayscale(image)
    
    
    if animal_type == "Dog":
        # dog vision -blue-yellow colorblindness
        img_animal = ImageOps.colorize(img_gray, black="#8B8682", white="#FFFF00")
    elif animal_type == "Cat":
        #  cat vision -kind of like grayscale
        img_animal = img_gray
    elif animal_type == "Bird":
        #  bird vision -enhanced UV perception
        img_animal = ImageEnhance.Brightness(img_gray).enhance(1.5)
    else:
        
        img_animal = img_gray
    
    return img_animal

# download image
def download_image(image, filename="image.jpg"):
    # Convert PIL image to bytes (if not the code runs into errors)
    img_bytes = image.tobytes()
    
    # Download file
    st.download_button(label="Download Image", data=img_bytes, file_name=filename)


st.title("🦄 Vision Simulator")

st.write("Color blindness refers to a condition where individuals have difficulty distinguishing certain colors. There are different types of color blindness, including:")

st.write("   💚 Deuteranopia: Green-blindness, making it challenging to differentiate between red and green colors.")
st.write("   ❤️ Protanopia: Red-blindness, causing difficulty in distinguishing between red and green colors.")
st.write("   💙 Tritanopia: Blue-blindness, leading to challenges in differentiating between blue and yellow colors.")

st.write("🦋 Animal Vision: Animals perceive colors differently from humans due to variations in their visual systems. The app simulates the vision of three different animals:")
st.write("   🐶 Dog: Simulates blue-yellow colorblindness, similar to certain types of human color blindness.")
st.write("   🐱 Cat: Vision similar to grayscale, lacking the vibrant colors perceived by humans.")
st.write("   🦜 Bird: Enhanced UV perception, allowing birds to see a broader spectrum of colors, including ultraviolet light")



uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# options for the dropdown
simulation_options = {
    "Normal Vision": "No visual impairment. Normal human vision.",
    "Deuteranopia": "Green-blindness. Difficulty in distinguishing between red and green colors.",
    "Protanopia": "Red-blindness. Difficulty in distinguishing between red and green colors.",
    "Tritanopia": "Blue-blindness. Difficulty in distinguishing between blue and yellow colors.",
    "Dog": "Simulated vision of a dog. Blue-yellow colorblindness.",
    "Cat": "Simulated vision of a cat. Similar to grayscale vision.",
    "Bird": "Simulated vision of a bird. Enhanced UV perception."
}

# selected images to choose from
st.subheader("Select a predefined image:")
image_options = {
    "Food": "images/food.jpg",
    "Dog": "images/dog.jpg",
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
   
    image = Image.open(uploaded_image)

# dropdown to select image
vision_type = st.selectbox("**😎 Select vision type:**", list(simulation_options.keys()))

# descriptions again
st.write(simulation_options[vision_type])

# here, just show the image that is being simulated
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
