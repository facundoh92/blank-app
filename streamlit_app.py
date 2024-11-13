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

# Step 1: Install gdown if necessary
try:
    import gdown
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "gdown"])

# Step 2: Download the file from Google Drive
file_url = "https://drive.google.com/uc?id=1zpT6gHzvbr21_Vq4NjpRY0JGSaQOSANa"
output_path = "fifa.zip"
gdown.download(file_url, output_path, quiet=False)

# Step 3: Unzip the file
with zipfile.ZipFile(output_path, 'r') as zip_ref:
    zip_ref.extractall("extracted_files")

# Step 4: Initialize the list to hold the paths of extracted files
extracted_files = []

# List all files in the extracted folder
for root, dirs, files in os.walk("extracted_files"):
    for file in files:
        extracted_files.append(os.path.join(root, file))

# Step 5: Sort the extracted files in ascending order by filename
extracted_files = sorted(extracted_files)

# Step 6: Find the first image file in sorted order
image_files = [f for f in extracted_files if f.lower().endswith(('jpg', 'jpeg', 'png'))]

if image_files:
    # Display the first image in the sorted list
    first_image_path = image_files[0]
    first_image = Image.open(first_image_path)
    st.image(first_image, caption=f"Displaying {os.path.basename(first_image_path)}", use_column_width=True)
else:
    st.write("No image files found in the extracted folder.")

st.write("List of extracted files:")
for file in extracted_files:
    st.write(file)
