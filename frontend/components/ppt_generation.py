import streamlit as st
import requests

def generate_ppt(user_inputs):
    st.subheader("🛠️ Generating AI-Powered Presentation...")

    try:
        response = requests.post("http://51.20.231.154:8000/generate_ppt", json=user_inputs, timeout=1000)
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