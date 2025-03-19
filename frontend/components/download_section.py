import requests  # ✅ FIXED: Importing requests library
import streamlit as st

import time  # ✅ Added for ensuring download verification

def download_ppt():
    if "ppt_filename" in st.session_state and st.session_state["ppt_filename"]:
        ppt_filename = st.session_state["ppt_filename"]
        ppt_url = f"http://51.20.231.154:8000/download_ppt/{ppt_filename}"

        # ✅ Show proper debug info
        st.write(f"📂 Debug: Stored PPT Filename: `{ppt_filename}`")
        
        # ✅ Add a download button
        st.markdown(f'<a href="{ppt_url}" download="{ppt_filename}">📥 Click here to Download PPT</a>', unsafe_allow_html=True)

        # ✅ Optional: Check if the file is accessible
        time.sleep(1)
        response = requests.get(ppt_url)
        if response.status_code == 404:
            st.error(f"❌ PPT file not found on server. Try regenerating the presentation.")

    else:
        st.warning("⚠️ No PPT available for download. Generate a new one first.")