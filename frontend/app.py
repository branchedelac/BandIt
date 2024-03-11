

import streamlit as st
import requests
import numpy as np
import os

st.set_page_config(
            page_title="BandIt", # => Quick reference - Streamlit
            page_icon="🎸",
            layout="centered" # wide
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

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

st.title("🎸 BandIt 🥁")

st.markdown("""## *It's time to make your rock dreams come true!*""")


with st.form("my_form"):
    st.write("Upload a midi file which has at least one guitar track.")
    file = st.file_uploader("File upload", type="mid", accept_multiple_files=False)

# Every form must have a submit button.
    submitted = st.form_submit_button("Submit")


    if submitted:
        st.write("Processing your file....")
        params = {}

        # TODO call our prediction API
        # Will the API return a midi file?
        #res = requests.get(url=base_url, params=params)

        # Show the result!
        st.write("Listen to your new drum track!")

# TODO Make use of this audio player snippet
# Do we need to convert the midi file to something else?
audio_file = open(f'{os.getcwd()}/frontend/Vår.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='mp3')

# Not sure what the below does...
sample_rate = 44100  # 44100 samples per second
seconds = 2  # Note duration of 2 seconds
frequency_la = 440  # Our played note will be 440 Hz
# Generate array with seconds*sample_rate steps, ranging between 0 and seconds
t = np.linspace(0, seconds, seconds * sample_rate, False)
# Generate a 440 Hz sine wave
note_la = np.sin(frequency_la * t * 2 * np.pi)
#st.audio(note_la, sample_rate=sample_rate)
