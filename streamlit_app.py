import streamlit as st

st.title("🎈 My new app")

#selected_nationality = st.selectbox("Select Nationality", "Select Position")
option = st.selectbox(
    "Elija una opcion:",
    ["Option 1", "Option 2", "Option 3"]
)
