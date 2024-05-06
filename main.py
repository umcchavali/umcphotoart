import streamlit as st

# Title
st.markdown('<h1 class="title">UMC Photoart</h1>', unsafe_allow_html=True)

# Tabs
tab1,tab2,tab3 = st.tabs(["About", "Gallery", "Shop"])

if tab1 == "About":
    
    st.write("About content goes here...")

elif tab2 == "Gallery":
    
    st.write("Gallery content goes here...")

elif tab3 == "Shop":
    
    st.write("Shop content goes here...")
