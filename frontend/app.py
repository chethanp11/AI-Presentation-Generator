import streamlit as st
import requests
from pptx import Presentation  # ✅ FIXED: Added missing import

st.set_page_config(page_title="AI PPT Generator", layout="wide")

# ------------------------- 🏠 HOME PAGE (Updated) -------------------------
def show_home():
    st.title("📊 AI-Powered Presentation Generator")
    st.write(
        """
        Welcome to the AI-Powered Presentation Generator!
        - Enter the **topic** and other details to create a high-quality PowerPoint.
        - Customize **audience, purpose, design, font preferences, and more**.
        - AI will refine your input and generate structured slides.
        - Feedback is used to **continuously improve** future presentations.
        """
    )
    st.markdown("---")

# -------------------------- 🧠 SESSION STATE CACHE --------------------------
if "topic" not in st.session_state:
    st.session_state["topic"] = "AI in Finance"

if "audience" not in st.session_state:
    st.session_state["audience"] = "General Public"

if "duration" not in st.session_state:
    st.session_state["duration"] = 20  # Default 20 minutes

if "num_slides" not in st.session_state:
    st.session_state["num_slides"] = 5  # Default 5 slides

if "purpose" not in st.session_state:
    st.session_state["purpose"] = "Explain how AI is used in finance."

if "design_style" not in st.session_state:
    st.session_state["design_style"] = "Minimalist"

if "font_choice" not in st.session_state:
    st.session_state["font_choice"] = "Arial"

if "color_scheme" not in st.session_state:
    st.session_state["color_scheme"] = "#000000"  # Default Black

if "bullet_style" not in st.session_state:
    st.session_state["bullet_style"] = "Dots"

if "additional_notes" not in st.session_state:
    st.session_state["additional_notes"] = ""

if "ppt_filename" not in st.session_state:
    st.session_state["ppt_filename"] = None
    
# ------------------------- ✏️ USER INPUT FORM -------------------------
def get_user_inputs():
    st.subheader("📋 Presentation Details")

    st.session_state["topic"] = st.text_input("🔹 Enter the Topic:", st.session_state["topic"])
    st.session_state["audience"] = st.selectbox("👥 Target Audience:", 
                                                ["General Public", "Executives", "Students", "Technical Team"],
                                                index=["General Public", "Executives", "Students", "Technical Team"].index(st.session_state["audience"]))
    st.session_state["duration"] = st.slider("⏳ Presentation Duration (minutes):", 5, 60, st.session_state["duration"])
    st.session_state["num_slides"] = st.slider("📑 Number of Slides:", 1, 20, st.session_state["num_slides"])
    st.session_state["purpose"] = st.text_area("🎯 Purpose of the Presentation", st.session_state["purpose"])

    st.subheader("🎨 Design Preferences")
    st.session_state["design_style"] = st.selectbox("🖌️ Choose Design Theme:", 
                                                    ["Minimalist", "Corporate", "Creative", "Bold"],
                                                    index=["Minimalist", "Corporate", "Creative", "Bold"].index(st.session_state["design_style"]))
    st.session_state["font_choice"] = st.selectbox("🔠 Font Preference:", 
                                                   ["Arial", "Calibri", "Times New Roman", "Open Sans"],
                                                   index=["Arial", "Calibri", "Times New Roman", "Open Sans"].index(st.session_state["font_choice"]))
    st.session_state["color_scheme"] = st.color_picker("🎨 Select Primary Color", st.session_state["color_scheme"])

    st.subheader("📝 Additional Customizations")
    st.session_state["bullet_style"] = st.selectbox("• Bullet Point Style:", 
                                                    ["Dots", "Numbers", "Checkmarks"],
                                                    index=["Dots", "Numbers", "Checkmarks"].index(st.session_state["bullet_style"]))
    st.session_state["additional_notes"] = st.text_area("✏️ Additional Notes (Optional)", st.session_state["additional_notes"])

    return {
        "topic": st.session_state["topic"],
        "audience": st.session_state["audience"],
        "duration": st.session_state["duration"],
        "num_slides": st.session_state["num_slides"],
        "purpose": st.session_state["purpose"],
        "design_style": st.session_state["design_style"],
        "font_choice": st.session_state["font_choice"],
        "color_scheme": st.session_state["color_scheme"],
        "bullet_style": st.session_state["bullet_style"],
        "additional_notes": st.session_state["additional_notes"]
    }

# ------------------------- 🚀 GENERATE PRESENTATION -------------------------
def generate_ppt(user_inputs):
    st.subheader("🛠️ Generating AI-Powered Presentation...")

    # Debugging: Print the request payload
    st.write("🔍 Debug: Sending Request to API")
    st.json(user_inputs)  # Show the exact JSON request

    try:
        response = requests.post("http://51.20.231.154:8000/generate_ppt", json=user_inputs, timeout=1000)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        
        if response.status_code == 200:
            st.success("✅ Presentation Created Successfully!")
            ppt_filename = response.json().get("file")
            st.session_state["ppt_filename"] = ppt_filename
        else:
            try:
                error_msg = response.json().get("detail", response.text)
            except ValueError:
                error_msg = response.text  # If response is not JSON

            st.error(f"❌ Failed to generate presentation. Error: {error_msg}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Could not connect to the API: {str(e)}")
        return

# ------------------------- 📥 DOWNLOAD PPT -------------------------
def download_ppt():
    if "ppt_filename" in st.session_state and st.session_state["ppt_filename"]:
        ppt_path = f"http://51.20.231.154:8000/download_ppt/{st.session_state['ppt_filename']}"
        st.markdown(f"[📥 Click here to Download PPT]({ppt_path})", unsafe_allow_html=True)
    else:
        st.warning("⚠️ No PPT available for download. Generate a new one first.")

# ------------------------- 🌟 MAIN EXECUTION -------------------------
show_home()
user_inputs = get_user_inputs()

if st.button("🚀 Generate PPT"):
    generate_ppt(user_inputs)

download_ppt()