import streamlit as st

def interactive_questions():
    st.title("🤖 AI-Guided Presentation Context")

    q1 = st.text_input("🔍 What is the main takeaway of your presentation?")
    q2 = st.text_input("🎯 What are the key points you want to highlight?")
    q3 = st.text_area("📖 Any additional details you want the AI to include?")
    
    if st.button("Submit Context"):
        st.success("✅ AI will use your responses to enhance slide generation.")