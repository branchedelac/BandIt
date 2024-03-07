import streamlit as st
import requests
'''
# BandIT
'''
base_url = ""

st.markdown('''
            Upload a midi file which has at least one guitar track.
            ''')

with st.form("my_form"):
    st.file_uploader("File upload", type="mid", accept_multiple_files=False)

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write("Processing your file....")
        params = {}
        #res = requests.get(url=base_url, params=params)
        st.write("Tada")
