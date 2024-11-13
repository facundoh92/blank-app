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
from PIL import Image

# Download and extract data function
def download_and_extract():
    # Google Drive file URL
    file_url = "https://drive.google.com/uc?id=1zpT6gHzvbr21_Vq4NjpRY0JGSaQOSANa"
    output_path = "fifa.zip"  # The path to save the downloaded zip file

    # Download the file using gdown
    st.write("Downloading the file...")
    gdown.download(file_url, output_path, quiet=False)

    # Unzip the file into the 'data' folder
    data_folder = "extracted_files"
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

    # Display one image from the extracted data
    # Assuming there are image files in the 'data' folder
    image_folder = "data"  # Folder where images are extracted
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

    if image_files:
        # Display the first image in the folder
        image_path = os.path.join(image_folder, image_files[0])
        image = Image.open(image_path)
        st.image(image, caption=f"Image: {image_files[0]}", use_column_width=True)
    else:
        st.write("No images found in the extracted folder.")

import streamlit as st
import os

# Function to display the folders in a given directory
def list_folders(directory):
    # List all directories in the specified path
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return folders

# Display the list of folders
st.title("Check Created Folders")

# Button to check folders in the current directory
if st.button("Check Folders"):
    # List the folders in the current directory or specify a path
    current_directory = os.getcwd()  # or use a specific directory like "data"
    folders = list_folders(current_directory)
    
    if folders:
        st.write("Created folders:")
        for folder in folders:
            st.write(folder)
    else:
        st.write("No folders found.")
