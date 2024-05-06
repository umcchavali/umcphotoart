import streamlit as st
import pandas as pd
import altair as alt
import pyperclip
from palettable.colorbrewer.qualitative import Set3_12

# Define color palettes
color_palettes = {
    "Set3": Set3_12.hex_colors,
    # Add more color palettes here...
}

# UI
st.title("Color Palette Recommender")

# Ask the user to select a color palette
selected_palette = st.selectbox("Select a color palette:", list(color_palettes.keys()))

# Display the selected palette
st.write(f"You selected: {selected_palette}")

# Define colors_df outside button condition
colors_df = pd.DataFrame(columns=['Color Name', 'Hex', 'Proportions'])

# Button to recommend colors
recommend_button = st.button("Recommend Colors")
if recommend_button:
    selected_colors = color_palettes[selected_palette]

    # Convert color data to DataFrame
    colors_df = pd.DataFrame({"Color Name": [f"Color {i}" for i in range(1, len(selected_colors) + 1)],
                              "Hex": selected_colors})

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
    cols = st.columns(len(selected_colors))
    for i, (color, hex_code) in enumerate(selected_colors):
        cols[i].color_picker(f"{color} - {hex_code}", hex_code)

# Button to copy color palette
copy_palette_button = st.button("Copy Color Palette")
if copy_palette_button and not colors_df.empty:
    palette_text = '\n'.join([f"{row['Color Name']}: {row['Hex']}" for index, row in colors_df.iterrows()])
    pyperclip.copy(palette_text)
    st.success("Color palette copied to clipboard!")
elif copy_palette_button and colors_df.empty:
    st.warning("No color palette to copy!")
