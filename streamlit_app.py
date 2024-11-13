import streamlit as st

st.title("🎈 My new app")

#selected_nationality = st.selectbox("Select Nationality", "Select Position")
option = st.selectbox(
    "Elija una opcion:",
    ["Option 1", "Option 2", "Option 3"]
)

import streamlit as st
import gdown
import zipfile
import os

# Download and extract data function
def download_and_extract():
    # Google Drive file URL
    file_url = "https://drive.google.com/uc?id=1zpT6gHzvbr21_Vq4NjpRY0JGSaQOSANa"
    output_path = "fifa.zip"  # The path to save the downloaded zip file

    # Download the file using gdown
    st.write("Downloading the file...")
    gdown.download(file_url, output_path, quiet=False)

    # Unzip the file into the 'data' folder
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)  # Create the folder if it doesn't exist

    st.write("Extracting the files...")
    with zipfile.ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall(data_folder)

    st.success(f"Files have been extracted to {data_folder}")

# Streamlit app UI
st.title("Streamlit File Download and Extraction")

# Button to start downloading and extracting
if st.button("Download and Extract FIFA Data"):
    download_and_extract()
