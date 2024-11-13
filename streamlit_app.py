import streamlit as st
from PIL import Image
import os
from model import model_interp,vae_loaded,show_interp
import torchvision
st.title("🎈 My new app prueba mensaje2")

#selected_nationality = st.selectbox("Select Nationality", "Select Position")
option = st.selectbox(
    "Elija una opcion:",
    ["Option 1", "Option 2", "Option 3"]
)


    # Display the first image in the sorted list

#first_image = Image.open('/workspaces/blank-app/extracted_files/Images/0.png')
#st.image(first_image, caption=f"Displaying {os.path.basename('/workspaces/blank-app/extracted_files/Images/0.png')}", use_column_width=True)

import pandas as pd
data = pd.read_csv("/workspaces/blank-app/filtered_data_fix2_withimages.csv")
filtered = data[data['Nationality'] == 'France']
filtered.to_csv('/workspaces/blank-app/filtered.csv', index=False)
names = list(filtered["Name"])
ids = list(filtered["realidnumber"])
#print(data)
#print(filtered)

print(names)
print(ids)

import random

index1 = 14
index2 = 42

interp_result = model_interp(model = vae_loaded, index1 = index1, index2 = index2).unbind(0)
imgs = [img.permute(1,2,0).cpu() for img in interp_result]
show_interp(imgs,index1,index2, scale=2);
