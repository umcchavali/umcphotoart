import streamlit as st
import pandas as pd
import altair as alt
import pyperclip

# Load color data
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('data/colors.csv', names=index, header=None)

# Define color palettes
color_palettes = {
    "Moody Green": [("Dark Green", "#006400"), ("Forest Green", "#228B22"),
                     ("Olive Green", "#808000"), ("Moss Green", "#8A9A5B")],
    "Pastel Colors": [("Pale Blue", "#afeeee"), ("Pale Pink", "#fadadd"),
                      ("Pale Green", "#98fb98"), ("Pale Lavender", "#dcd0ff")],
    "Vivid Bright Colors": [("Red", "#ff0000"), ("Yellow", "#ffff00"),
                             ("Blue", "#0000ff"), ("Green", "#008000")],
    "Orange Palette": [("Orange Red", "#ff4500"), ("Dark Orange", "#ff8c00"),
                       ("Gold", "#ffd700"), ("Tomato", "#ff6347")],
    "Purple Palette": [("Indigo", "#4b0082"), ("Purple", "#800080"),
                       ("Orchid", "#da70d6"), ("Lavender", "#e6e6fa")],
    "Pink Palette": [("Hot Pink", "#ff69b4"), ("Deep Pink", "#ff1493"),
                     ("Pale Violet Red", "#db7093"), ("Medium Orchid", "#ba55d3")],
    "Black & White": [("Black", "#000000"), ("Gray", "#808080"),
                      ("White", "#ffffff"), ("Silver", "#c0c0c0")],
    "Brown Palette": [("Sienna", "#a0522d"), ("Saddle Brown", "#8b4513"),
                      ("Chocolate", "#d2691e"), ("Tan", "#d2b48c")],
    "Rainbow Colors": [("Red", "#ff0000"), ("Orange", "#ffa500"),
                       ("Yellow", "#ffff00"), ("Green", "#008000"),
                       ("Blue", "#0000ff"), ("Indigo", "#4b0082"),
                       ("Violet", "#8a2be2")],
    # Add more color palettes here...
}

# UI
st.title("Color Palette Recommender")

# Ask the user to select their favorite genre of colors
selected_genre = st.selectbox("Select your favorite genre of colors:", list(color_palettes.keys()))

# Display the selected genre
st.write(f"You selected: {selected_genre}")

# Define colors_df outside button condition
colors_df = pd.DataFrame(columns=['Color Name', 'Hex', 'Proportions'])

# Button to recommend colors
recommend_button = st.button(f"Recommend Colors for {selected_genre}")
if recommend_button:
    recommended_colors = color_palettes[selected_genre]

    # Convert color data to DataFrame
    colors_df = pd.DataFrame(recommended_colors, columns=['Color Name', 'Hex'])

    # Check if DataFrame is not empty
    if not colors_df.empty:
        # Create Altair bar chart
        chart = alt.Chart(colors_df).mark_bar().encode(
            x=alt.X('Color Name:N', axis=None),
            y=alt.Y('Color Name:N', sort='-x', scale=alt.Scale(domain=list(colors_df['Color Name']))),
            color=alt.Color('Color Name:N', scale=None),
            tooltip=['Color Name:N', 'Hex:N']
        ).properties(
            title="Recommended Colors",
            width=500,
            height=300
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

        # Display recommended colors as color pickers horizontally
        st.subheader("Recommended Colors")
        cols = st.columns(len(recommended_colors))
        for i, (color, hex_code) in enumerate(recommended_colors):
            cols[i].color_picker(f"{color} - {hex_code}", hex_code)

    # Create area chart underneath the color pickers
    area_chart = alt.Chart(colors_df).mark_area(
        interpolate='step-after',
        line=True
    ).encode(
        x=alt.X('Color Name:N', sort='-x', axis=alt.Axis(labels=False)),
        y=alt.Y('count()', axis=None),
        color=alt.Color('Color Name:N', scale=None),
        tooltip=['Color Name:N', 'Hex:N']
    ).properties(
        title="Recommended Colors",
        width=500,
        height=100
    ).interactive()

    st.altair_chart(area_chart, use_container_width=True)

# Button to copy color palette
copy_palette_button = st.button("Copy Color Palette")
if copy_palette_button and not colors_df.empty:
    palette_text = '\n'.join([f"{row['Color Name']}: {row['Hex']}" for index, row in colors_df.iterrows()])
    pyperclip.copy(palette_text)
    st.success("Color palette copied to clipboard!")
elif copy_palette_button and colors_df.empty:
    st.warning("No color palette to copy!")
