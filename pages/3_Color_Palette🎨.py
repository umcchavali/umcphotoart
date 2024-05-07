import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load the colors dataset
csv = pd.read_csv("data/colors.csv")

# Function to convert RGB values to hexadecimal format
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Function to generate complementary color palette
def generate_complementary_palette(color):
    complementary_color = tuple(255 - value for value in color)
    return [color, complementary_color]

# Function to generate analogous color palette
def generate_analogous_palette(color):
    step = 30
    analogous_colors = [(color[0], color[1], max(0, min(255, color[2] + (i * step)))) for i in range(-2, 3)]
    return analogous_colors

# Function to generate triadic color palette
def generate_triadic_palette(color):
    step = 120
    triadic_colors = [(color[0], max(0, min(255, color[1] + (i * step))), max(0, min(255, color[2] + (i * step)))) for i in range(0, 3)]
    return triadic_colors

# Function to display color palette
def display_color_palette(palette, palette_type):
    fig, ax = plt.subplots(1, len(palette), figsize=(12, 2))
    for i, color in enumerate(palette):
        ax[i].add_patch(Rectangle((0, 0), 1, 1, color=rgb_to_hex(color)))
        ax[i].axis('off')
        ax[i].text(0.5, -0.3, f"{palette_type} {i+1}\n{rgb_to_hex(color)}", ha="center", transform=ax[i].transAxes)
    plt.tight_layout()
    st.pyplot(fig)

# Title of the app
st.title("🌈 Color Palette Generator")

st.write("🍭 Hey there! Ever heard of color theory? It's like the science behind the rainbow, helping us understand how colors work together to create different moods and effects. From the way they complement each other to the emotions they evoke, color theory is like a secret code that artists and designers use to make their creations pop!")
st.write("🔴 Primary Colors: Red, blue, and yellow are considered primary colors because they cannot be created by mixing other colors. They are fundamental for creating all other colors in the color wheel.")
st.write("🟠 Secondary Colors: Orange, green, and purple are secondary colors. They are created by mixing two primary colors together. For example, mixing red and blue creates purple.")
st.write("🟡 Complementary Colors: Complementary colors are pairs of colors that are opposite each other on the color wheel. When placed next to each other, they create contrast and make each other appear more vibrant.")
st.write("🟢 Analogous Colors: Analogous colors are groups of colors that are adjacent to each other on the color wheel. They usually share similar hues and create a harmonious color scheme when used together.")
st.write("🔵 Triadic Colors: Triadic colors are three colors that are evenly spaced around the color wheel. They provide a balanced and vibrant color scheme when used together, as they offer a good contrast while maintaining harmony.")



# Dropdown menu to select a color
selected_color = st.selectbox("Choose a Color 👇", csv['color_name'].unique())

if selected_color:
    selected_row = csv[csv['color_name'] == selected_color].iloc[0]
    selected_color_rgb = (selected_row['r'], selected_row['g'], selected_row['b'])
    
    st.subheader(f"Selected Color: {selected_color}")
    st.write(f"RGB Values: {selected_color_rgb}")
    st.write(f"Hexadecimal Value: {rgb_to_hex(selected_color_rgb)}")

    st.subheader("Color Palettes")

   
    st.subheader("Complementary Palette")
    complementary_palette = generate_complementary_palette(selected_color_rgb)
    display_color_palette(complementary_palette, "Complementary")

    st.subheader("Analogous Palette")
    analogous_palette = generate_analogous_palette(selected_color_rgb)
    display_color_palette(analogous_palette, "Analogous")

    st.subheader("Triadic Palette")
    triadic_palette = generate_triadic_palette(selected_color_rgb)
    display_color_palette(triadic_palette, "Triadic")
