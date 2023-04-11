import os
import random
import pandas as pd
import streamlit as st
import shutil

CSV_DATA_FOLDER = 'csv_data'
CSV_HASIL_FOLDER = 'hasil'
CSV_JELEK = 'jelek'
ACTION_CSV_FILE = 'action.csv'

if not os.path.exists(CSV_HASIL_FOLDER):
    os.makedirs(CSV_HASIL_FOLDER)

if not os.path.exists(CSV_JELEK):
    os.makedirs(CSV_JELEK)

csv_fold = [f for f in os.listdir(CSV_DATA_FOLDER) if f.endswith('.csv')]
hasil = [f for f in os.listdir(CSV_HASIL_FOLDER) if f.endswith('.csv')]
jelek = [f for f in os.listdir(CSV_JELEK) if f.endswith('.csv')]
csv_files = [x for x in csv_fold if x not in hasil and x not in jelek]
if(len(csv_files) > 0):
    csv_x = random.choice(csv_files)

    csv_path = os.path.join(CSV_DATA_FOLDER, csv_x)
    df = pd.read_csv(csv_path)

    st.write("Data: "+str(len(csv_fold) - len(csv_files)) + "/" + str(len(csv_fold)))
    st.dataframe(df)

    save = st.button('Save')
    no_save = st.button("No save")
    if save:
        csv_files.remove(csv_x)
        df.to_csv(os.path.join("hasil", csv_x))
        csv_x = random.choice(csv_files)

    if no_save:
        csv_files.remove(csv_x)
        df.to_csv(os.path.join("jelek", csv_x))
        csv_x = random.choice(csv_files)
else:
    st.write("Tidak ada yang perlu di kurasi lagi, terimakasih!")
if(st.button("ZIP")):
    shutil.make_archive("hasil", "zip", CSV_HASIL_FOLDER)

button_text = "Download Zip File"
button_kwargs = {"key": "download_button"}

if os.path.isfile("hasil.zip"):
    with open("hasil.zip", "rb") as f:
        bytes_data = f.read()
        st.download_button(button_text, data=bytes_data,
                        file_name="hasil.zip", **button_kwargs)


if(st.button("Delete ZIP")):
    os.remove("hasil.zip")
