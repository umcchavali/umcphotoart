
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
# Load color data from CSV file
@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv)
    return df

# Load color data
index=["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('data/colors.csv', names=index, header=None)
# Function to recommend colors based on selected genre
def recommend_colors(genre):
    # Logic to recommend colors based on the selected genre
    recommended_colors = []

    if genre == "Moody Green":
        # Recommendation logic for moody green colors
        recommended_colors = [("Dark Green", "#006400"), ("Forest Green", "#228B22"), 
                              ("Olive Green", "#808000"), ("Moss Green", "#8A9A5B")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Pastel Colors":
        # Recommendation logic for pastel colors
        recommended_colors = [("Pale Blue", "#afeeee"), ("Pale Pink", "#fadadd"), 
                              ("Pale Green", "#98fb98"), ("Pale Lavender", "#dcd0ff")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Vivid Bright Colors":
        # Recommendation logic for vivid bright colors
        recommended_colors = [("Red", "#ff0000"), ("Yellow", "#ffff00"), 
                              ("Blue", "#0000ff"), ("Green", "#008000")]
        proportions = [0.25, 0.25, 0.25, 0.25]
    elif genre == "Soft Neutrals":
        # Recommendation logic for soft neutral colors
        recommended_colors = [("Beige", "#f5f5dc"), ("Light Gray", "#d3d3d3"), 
                              ("Warm Gray", "#a9a9a9"), ("Taupe", "#483c32")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Earthy Tones":
        # Recommendation logic for earthy tones
        recommended_colors = [("Terracotta", "#e2725b"), ("Burnt Orange", "#cc5500"), 
                              ("Sienna", "#a0522d"), ("Chocolate", "#d2691e")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Ocean Blues":
        # Recommendation logic for ocean blue colors
        recommended_colors = [("Turquoise", "#40e0d0"), ("Aquamarine", "#7fffd4"), 
                              ("Sky Blue", "#87ceeb"), ("Cerulean", "#007ba7")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Sunset Palette":
        # Recommendation logic for sunset palette colors
        recommended_colors = [("Coral", "#ff7f50"), ("Peach", "#ffdab9"), 
                              ("Goldenrod", "#daa520"), ("Burnt Sienna", "#e97451")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Monochrome":
        # Recommendation logic for monochrome colors
        recommended_colors = [("Black", "#000000"), ("Gray", "#808080"), 
                              ("Silver", "#c0c0c0"), ("White", "#ffffff")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Autumn Colors":
        # Recommendation logic for autumn colors
        recommended_colors = [("Maroon", "#800000"), ("Saffron", "#f4c430"), 
                              ("Rust", "#b7410e"), ("Olive", "#808000")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    elif genre == "Spring Blossoms":
        # Recommendation logic for spring blossom colors
        recommended_colors = [("Lilac", "#c8a2c8"), ("Mauve", "#e0b0ff"), 
                              ("Pastel Yellow", "#fdfd96"), ("Baby Pink", "#f4c2c2")]
        proportions = [0.4, 0.3, 0.2, 0.1]
    else:
        # Default recommendation
        recommended_colors = [("Red", "#ff0000"), ("Yellow", "#ffff00"), 
                              ("Blue", "#0000ff"), ("Green", "#008000")]
        proportions = [0.25, 0.25, 0.25, 0.25]

    return recommended_colors, proportions

# Function to create histogram chart
def create_histogram(recommended_colors, proportions):
    # Plotting
    fig, ax = plt.subplots()
    for i, (color_name, color_hex) in enumerate(recommended_colors):
        ax.add_patch(mpatches.Rectangle((0, i), proportions[i], 0.8, color=color_hex, label=color_name))
        ax.text(proportions[i] + 0.01, i + 0.4, color_name, va="center", ha="left")
        ax.text(proportions[i] + 0.01, i + 0.1, color_hex, va="center", ha="left", fontsize=9, color="grey")
    
    ax.set_xlim(0, 1.1)
    ax.set_ylim(-0.5, len(recommended_colors) - 0.5)
    ax.set_xlabel("Proportions")
    ax.set_ylabel("Colors")
    ax.set_title("Recommended Color Proportions")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.axis('off')
    st.pyplot(fig)

# UI
st.title("Color Palette Recommender")

# Ask the user to select their favorite genre of colors
selected_genre = st.selectbox("Select your favorite genre of colors:",
                              ["Moody Green", "Pastel Colors", "Vivid Bright Colors",
                               "Soft Neutrals", "Earthy Tones", "Ocean Blues",
                               "Sunset Palette", "Monochrome", "Autumn Colors",
                               "Spring Blossoms", "Other"])

# Display the selected genre
st.write(f"You selected: {selected_genre}")

# Button to recommend colors
if st.button("Recommend Colors"):
    recommended_colors, proportions = recommend_colors(selected_genre)
    
    # Display the recommended colors
    st.write("Recommended colors:")
    for color_name, _ in recommended_colors:
        st.write(color_name)
    
    # Create histogram chart
    create_histogram(recommended_colors, proportions)
