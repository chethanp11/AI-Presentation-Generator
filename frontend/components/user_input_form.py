import streamlit as st

def get_user_inputs():
    st.subheader("📋 Presentation Details")

    topic = st.text_input("🔹 Enter the Topic:", "AI in Finance")
    audience = st.selectbox("👥 Target Audience:", ["General Public", "Executives", "Students", "Technical Team"])
    duration = st.slider("⏳ Presentation Duration (minutes):", 5, 60, 20)
    num_slides = st.slider("📑 Number of Slides:", 1, 20, 5)
    purpose = st.text_area("🎯 Purpose of the Presentation", "Explain how AI is used in finance.")

    st.subheader("🎨 Design Preferences")
    design_style = st.selectbox("🖌️ Choose Design Theme:", ["Minimalist", "Corporate", "Creative", "Bold"])
    font_choice = st.selectbox("🔠 Font Preference:", ["Arial", "Calibri", "Times New Roman", "Open Sans"])
    color_scheme = st.color_picker("🎨 Select Primary Color")

    st.subheader("📝 Additional Customizations")
    bullet_style = st.selectbox("• Bullet Point Style:", ["Dots", "Numbers", "Checkmarks"])
    additional_notes = st.text_area("✏️ Additional Notes (Optional)")

    return {
        "topic": topic,
        "audience": audience,
        "duration": duration,
        "num_slides": num_slides,
        "purpose": purpose,
        "design_style": design_style,
        "font_choice": font_choice,
        "color_scheme": color_scheme,
        "bullet_style": bullet_style,
        "additional_notes": additional_notes
    }