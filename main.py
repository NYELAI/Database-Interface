import streamlit as st

st.set_page_config(page_title="Main Page", layout="centered")


st.title("Astra DB CRUD Operations with Streamlit")

# Adding radio buttons for database selection
db_choice = st.radio(
    "Select Database Environment:",
    ('Production Database', 'Development')
)