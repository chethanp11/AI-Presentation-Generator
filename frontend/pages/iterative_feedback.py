import streamlit as st

def iterative_feedback():
    st.title("🔁 Improve Your Presentation Iteratively")

    feedback = st.text_area("📝 Provide feedback to improve the PPT", "")
    
    if st.button("Submit Feedback"):
        st.success("✅ Feedback submitted! AI will use this to improve the next version.")