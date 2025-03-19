import streamlit as st
from components.user_input_form import get_user_inputs
from components.ppt_generation import generate_ppt
from components.download_section import download_ppt
from pages.upload_template import upload_template
from pages.iterative_feedback import iterative_feedback
from pages.interactive_questions import interactive_questions

st.set_page_config(page_title="AI PPT Generator", layout="wide")

# ------------------------- 🏠 HOME PAGE -------------------------
def show_home():
    st.title("📊 AI-Powered Presentation Generator")
    st.write("""
        Welcome to the AI-Powered Presentation Generator!
        - Enter the **topic** and other details to create a high-quality PowerPoint.
        - Customize **audience, purpose, design, font preferences, and more**.
        - AI will refine your input and generate structured slides.
        - Feedback is used to **continuously improve** future presentations.
    """)
    st.markdown("---")

# ------------------------- 🌟 MAIN EXECUTION -------------------------
show_home()
user_inputs = get_user_inputs()

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Generate PPT"):
        generate_ppt(user_inputs)

with col2:
    download_ppt()

# Navigation links for additional features
st.sidebar.title("📌 Additional Features")
st.sidebar.page_link("pages/upload_template.py", label="📤 Upload PPT Template")
st.sidebar.page_link("pages/iterative_feedback.py", label="🔁 Improve PPT Iteratively")
st.sidebar.page_link("pages/interactive_questions.py", label="🤖 AI-Guided Context Gathering")