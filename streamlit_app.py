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

# Step 4: List extracted files
#st.write("Files extracted:")
#for root, dirs, files in os.walk("extracted_files"):
#    for file in files:
#        st.write(file)
