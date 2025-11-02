import openai
import re

from backend.db_handler import retrieve_common_feedback, store_ai_feedback

class RequirementEnricher:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_slide_titles(self, topic, num_slides):
        """
        Forces AI to generate exactly `num_slides` unique slide titles.
        """
        enriched_prompt = f"""
        You are an AI expert creating a PowerPoint on **"{topic}"**.
        Generate **{num_slides} unique, structured slide titles**.

        **Rules:**
        - Each slide must focus on a different aspect of the topic.
        - **Do NOT summarize**. Ensure diverse subtopics.
        - Titles should be **concise, specific, and engaging** (Max 6 words).
        - Follow a **logical progression** from introduction to key insights.

        **Output Format:**
        1. Slide Title
        2. Slide Title
        3. Slide Title
        ...
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": enriched_prompt}]
            )
            slide_titles_raw = response.choices[0].message.content.split("\n")

            # ✅ **Ensure Correct Slide Count**
            slide_titles = []
            for title in slide_titles_raw:
                cleaned = title.strip()
                if not cleaned:
                    continue
                cleaned = re.sub(r"^\d+[\).\s-]*", "", cleaned).strip()
                if cleaned:
                    slide_titles.append(cleaned)

            if len(slide_titles) < num_slides:
                raise ValueError(f"⚠️ AI returned {len(slide_titles)} slides instead of {num_slides}. Retrying...")

            return slide_titles[:num_slides]
        except Exception as e:
            return [f"Slide {i+1}: {topic}" for i in range(num_slides)]  # Fallback

    def enrich_prompt(self, topic, audience, duration, purpose, num_slides):
        """
        Forces AI to generate exactly `num_slides` structured slides.
        """
        try:
            past_feedback_entries = retrieve_common_feedback(topic)
            if past_feedback_entries:
                past_feedback = "; ".join(past_feedback_entries)
            else:
                past_feedback = "No relevant feedback found."
        except Exception as e:
            past_feedback = f"⚠️ Error retrieving past feedback: {str(e)}"

        refined_prompt = f"""
        You are creating a **{num_slides}-slide** PowerPoint on **"{topic}"**.
        - 🎯 **Audience:** {audience}
        - ⏳ **Duration:** {duration} minutes
        - 📌 **Purpose:** {purpose}
        - 📊 **Past Feedback Considered:** {past_feedback}

        **Rules:**
        - Generate **EXACTLY {num_slides} slides** (No more, no less).
        - **Each slide MUST be a unique subtopic** (No summarization).
        - Use **clear bullet points**, not paragraphs.
        - **No duplicate content** across slides.

        **Expected Output Format:**
        Slide 1: **Title**
        - Bullet 1
        - Bullet 2
        - Bullet 3

        Slide 2: **Title**
        - Bullet 1
        - Bullet 2
        - Bullet 3

        Slide 3: **Title**
        - Bullet 1
        - Bullet 2
        - Bullet 3

        Slide {num_slides}: **Conclusion**
        - Bullet 1
        - Bullet 2
        - Bullet 3
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": refined_prompt}]
            )
            enriched_content = response.choices[0].message.content

            # ✅ **Check for Correct Slide Count**
            generated_slides = enriched_content.split("\n\n")
            if len(generated_slides) != num_slides:
                raise ValueError(f"⚠️ AI returned {len(generated_slides)} slides instead of {num_slides}. Regenerating...")

            # ✅ Store AI-generated feedback for future improvements
            if topic.strip():
                store_ai_feedback(topic, 0, enriched_content)

            return enriched_content
        except Exception as e:
            return f"⚠️ Error generating enriched content: {str(e)}"
