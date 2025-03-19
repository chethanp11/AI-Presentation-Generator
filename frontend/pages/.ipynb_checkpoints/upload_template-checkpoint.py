import streamlit as st

def upload_template():
    st.title("📤 Upload Your PPT Template")
    
    uploaded_file = st.file_uploader("Upload a PowerPoint template (.pptx)", type=["pptx"])
    
    if uploaded_file:
        st.success("✅ Template Uploaded Successfully!")
        st.session_state["ppt_template"] = uploaded_file  # Save for further processing