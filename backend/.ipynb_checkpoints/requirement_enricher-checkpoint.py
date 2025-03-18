import openai
import os
from backend.db_handler import retrieve_common_feedback, store_ai_feedback, store_user_feedback
from pptx import Presentation  # ✅ FIXED: Added missing import

class RequirementEnricher:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def enrich_prompt(self, topic, audience, duration, purpose):
        """
        Enhances user input using GPT-4o and past feedback.
        - Retrieves past feedback to refine content.
        - Generates structured slides with AI guidance.
        """

        # ✅ FIX: Ensure `past_feedback` does not break the system
        try:
            past_feedback = retrieve_common_feedback(topic)
            if not past_feedback:
                past_feedback = "No relevant feedback found."
        except Exception as e:
            past_feedback = f"⚠️ Error retrieving past feedback: {str(e)}"

        # ✅ IMPROVED PROMPT: Structured & Clear
        enriched_prompt = f"""
        You are an expert AI content generator specializing in PowerPoint presentations.
        A user is creating a PowerPoint on **"{topic}"**.

        - **Target Audience:** {audience}
        - **Presentation Duration:** {duration} minutes
        - **Objective:** {purpose}
        
        **Past User & AI Feedback on Similar Topics:**
        {past_feedback}

        **Your Task:**
        - Generate a structured breakdown for slides.
        - Use **bullet points** instead of paragraphs.
        - Suggest **concise, engaging, and professional** slide content.
        - Provide **visual recommendations** (icons, images, charts).
        - **Avoid GPT-style conversations.** Keep it structured & crisp.

        **Expected Output Format:**
        1️⃣ **Title Slide:** Topic & Introduction  
        2️⃣ **Key Subtopics** with bullet points  
        3️⃣ **Visual Enhancements** for each slide  
        4️⃣ **No conversational responses.**  
        """

        # ✅ FIX: Catch GPT API Failures
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": enriched_prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error generating enriched prompt: {str(e)}"