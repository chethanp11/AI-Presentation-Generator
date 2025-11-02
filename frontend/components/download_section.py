import requests  # ✅ FIXED: Importing requests library
import streamlit as st

from frontend.utils.api_handler import get_backend_base_url

def download_ppt():
    if "ppt_filename" in st.session_state and st.session_state["ppt_filename"]:
        ppt_filename = st.session_state["ppt_filename"]
        base_url = get_backend_base_url()
        ppt_url = f"{base_url}/download_ppt/{ppt_filename}"

        # ✅ Show proper debug info
        st.write(f"📂 Debug: Stored PPT Filename: `{ppt_filename}`")
        
        # ✅ Add a download button
        st.markdown(f'<a href="{ppt_url}" download="{ppt_filename}">📥 Click here to Download PPT</a>', unsafe_allow_html=True)

        # ✅ Optional: Check if the file is accessible
        try:
            response = requests.head(ppt_url, timeout=5)
            if response.status_code == 404:
                st.error("❌ PPT file not found on server. Try regenerating the presentation.")
        except requests.RequestException:
            st.warning("⚠️ Unable to verify PPT availability. Download may still succeed.")

    else:
        st.warning("⚠️ No PPT available for download. Generate a new one first.")
