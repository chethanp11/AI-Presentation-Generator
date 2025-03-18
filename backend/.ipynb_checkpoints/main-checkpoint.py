from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import openai
from pptx import Presentation
import os
from backend.format_ppt import apply_formatting  # Import formatting function

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI Backend is Running!"}
    
# Define output directory
OUTPUT_DIR = "/home/ubuntu/AI-Presentation-Generator/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists

# Request Model for API
class PresentationRequest(BaseModel):
    topic: str
    num_slides: int

# Load OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY as an environment variable.")

client = openai.OpenAI(api_key=openai_api_key)

@app.post("/generate_ppt")
def generate_ppt(request: PresentationRequest):
    try:
        filename = f"{request.topic.replace(' ', '_')}_presentation.pptx"
        file_path = os.path.join(OUTPUT_DIR, filename)

        # Delete existing file
        if os.path.exists(file_path):
            os.remove(file_path)

        prs = Presentation()
        for i in range(request.num_slides):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Generate slide {i+1} on {request.topic}"}]
            )
            slide_content = response.choices[0].message.content

            slide = prs.slides.add_slide(prs.slide_layouts[5])
            title = slide.shapes.title
            title.text = slide_content

        # Apply formatting before saving
        apply_formatting(prs)

        prs.save(file_path)

        print(f"Presentation created: {file_path}")  # Show filename in logs

        return {"message": "Presentation created successfully", "file": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presentation: {str(e)}")

@app.get("/download_ppt/{filename}")
def download_ppt(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Presentation file not found.")
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=filename)