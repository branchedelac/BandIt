import streamlit as st
import requests
import numpy as np
import os

temp_data_folder = os.path.join(os.getcwd(), "backend/temp_data")
dev_url = "http://127.0.0.1:8000"
prod_url = "https://bandit-ydlcssklqq-ew.a.run.app"


st.set_page_config(
    page_title="BandIt",  # => Quick reference - Streamlit
    page_icon="🎸",
    layout="centered",  # wide
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=New+Rocker&display=swap');

h1 {
    font-family:  "New Rocker", system-ui;
    font-size: 80px;
    font-weight: 400;
    font-style: normal;
    text-align: center;
    padding-bottom: 20px;

}
h2 {
    font-style: italic;
    font-size: 20px;
    text-align: center;
    padding-bottom: 40px;

}


"""

st.write(f"<style>{CSS}</style>", unsafe_allow_html=True)

st.title("🎸 BandIt 🥁")

st.markdown("""## *It's time to make your rock dreams come true!*""")


with st.form("upload"):
    st.write("Upload a midi file which contains at least one guitar track!")
    file = st.file_uploader("File upload", type="mid", accept_multiple_files=False)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Upload file")

if submitted:
    with st.spinner("Processing your file... 🎶"):
        try:
            response = requests.request("POST", f"{dev_url}/predict-progressive", files={"file": file})
        except Exception:
            response = requests.request("POST", f"{prod_url}/predict-progressive", files={"file": file})
    st.success('Processing complete! 🎉')

    # Show the result!
    if response.status_code == 200:
        st.write(f"**Drum track successfully generated for {file.name}!**")
        st.write("Listen to your new drum arrangement below!")
        audio_file = open(
            os.path.join(temp_data_folder, "drums.wav"), "rb"
        )
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="wav")

        st.write(f"Download your drum arrangement as a midi file!")
        with open(
            os.path.join(temp_data_folder, "drums.mid"), "rb"
        ) as new_midi:
            downloaded = st.download_button(
                label="Download",
                data=new_midi,
                file_name=f"{file.name[:-4]}_drums.mid",
                mime="audio/midi"
            )
    else:
        st.error(f"Something went wrong! Status: {response.status_code}")
