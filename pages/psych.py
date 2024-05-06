import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load the colors dataset
colors_df = pd.read_csv("data/colors.csv")

# Function to convert RGB values to hexadecimal format
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Function to display color information
def display_color_info(color):
    row = colors_df[colors_df['Color'] == color].iloc[0]
    rgb = (row['R'], row['G'], row['B'])
    hex_color = rgb_to_hex(rgb)

    st.subheader(f"Selected Color: {color}")
    st.write(f"RGB Values: {rgb}")
    st.write(f"Hexadecimal Value: {hex_color}")

    # Display the color
    fig, ax = plt.subplots()
    ax.add_patch(Rectangle((0, 0), 1, 1, color=hex_color))
    ax.axis('off')
    st.pyplot(fig)

    # Display some basic color psychology information
    st.write("**Color Psychology Information:**")
    st.write("- Symbolic Meaning: " + row['Symbolic Meaning'])
    st.write("- Cultural Significance: " + row['Cultural Significance'])
    st.write("- Psychological Effects: " + row['Psychological Effects'])

# Title of the app
st.title("Color Psychology Analyzer")
st.sidebar.title("Select a Color")

# Dropdown menu to select a color
selected_color = st.sidebar.selectbox("Choose a Color", colors_df['Color'].unique())

if selected_color:
    display_color_info(selected_color)
