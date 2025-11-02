import requests
import streamlit as st

from frontend.utils.api_handler import get_backend_base_url

def generate_ppt(user_inputs):
    st.subheader("🛠️ Generating AI-Powered Presentation...")

    base_url = get_backend_base_url()
    endpoint = f"{base_url}/generate_ppt"

    try:
        response = requests.post(endpoint, json=user_inputs, timeout=1000)
        response.raise_for_status()

        if response.status_code == 200:
            st.success("✅ Presentation Created Successfully!")
            ppt_filename = response.json().get("file")
            st.session_state["ppt_filename"] = ppt_filename
        else:
            error_msg = response.json().get("detail", response.text)
            st.error(f"❌ Failed to generate presentation. Error: {error_msg}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Could not connect to the API: {str(e)}")
