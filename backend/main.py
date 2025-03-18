import os
import openai
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from pptx import Presentation
from pptx.util import Inches  # ✅ FIXED: Ensure dimensions are handled properly
from backend.format_ppt import apply_formatting
from backend.requirement_enricher import RequirementEnricher
from backend.db_handler import store_ai_feedback, store_user_feedback, retrieve_common_feedback

# ------------------------- 🚀 Initialize FastAPI App -------------------------
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Backend is Running!"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")

# ------------------------- 📁 File Paths -------------------------
OUTPUT_DIR = "/home/ubuntu/AI-Presentation-Generator/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------- 🤖 Load OpenAI API Key -------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY as an environment variable.")

client = openai.OpenAI(api_key=openai_api_key)
enricher = RequirementEnricher(api_key=openai_api_key)

# ------------------------- 📄 Request Model -------------------------
class PresentationRequest(BaseModel):
    topic: str = Field(..., example="AI in Finance")
    num_slides: int = Field(..., ge=1, le=20, example=5)
    audience: str = Field(default="General Public")
    duration: int = Field(default=20)
    purpose: str = Field(default="Explain how AI is used in finance.")
    design_style: str = Field(default="Minimalist")
    font_choice: str = Field(default="Arial")
    color_scheme: str = Field(default="#000000")
    bullet_style: str = Field(default="Dots")
    additional_notes: str = Field(default="")

# ------------------------- 📝 Generate PPT -------------------------
@app.post("/generate_ppt")
def generate_ppt(request: PresentationRequest):
    try:
        print(f"🟢 Generating PPT for topic: {request.topic} | Slides: {request.num_slides}")

        filename = f"{request.topic.replace(' ', '_')}_presentation.pptx"
        file_path = os.path.join(OUTPUT_DIR, filename)

        # Delete existing file
        if os.path.exists(file_path):
            os.remove(file_path)

        prs = Presentation()
        gpt_feedback = ""

        for i in range(request.num_slides):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Generate slide {i+1} on {request.topic}"}]
            )

            slide_content = response.choices[0].message.content
            if not slide_content:
                raise ValueError(f"GPT-4o did not return content for slide {i+1}")

            # Add slide
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            title = slide.shapes.title
            title.text = f"Slide {i+1}: {request.topic}"

            # ✅ FIX: Properly add text box and set text without using width/height on TextFrame
            left = Inches(1)  # 1 inch from left
            top = Inches(1.5)  # 1.5 inches from top
            width = Inches(8)  # Width of text box
            height = Inches(4)  # Height of text box
            
            # Add a textbox shape (width and height should be set here, NOT on text_frame)
            text_box = slide.shapes.add_textbox(left, top, width, height)
            text_frame = text_box.text_frame  # Get text frame inside the box
            text_frame.text = slide_content  # Assign text to text frame

            # ✅ Set TextFrame Margins to Keep Content Inside Layout
            text_frame.margin_left = Inches(0.2)
            text_frame.margin_right = Inches(0.2)
            text_frame.margin_top = Inches(0.2)
            text_frame.margin_bottom = Inches(0.2)
            
            # ✅ Auto-size text box if needed (Prevents overflow)
            text_frame.word_wrap = True

            gpt_feedback += f"Slide {i+1} feedback: {slide_content}\n"

        # Apply formatting
        apply_formatting(prs, gpt_feedback)

        prs.save(file_path)
        print(f"📂 Presentation saved at {file_path}")

        return {"message": "✅ Presentation created successfully", "file": filename, "gpt_feedback": gpt_feedback}

    except Exception as e:
        print(f"❌ Error generating presentation: {str(e)}")  # Log error
        raise HTTPException(status_code=500, detail=f"❌ Error generating presentation: {str(e)}")