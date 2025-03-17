from fastapi import FastAPI
from pydantic import BaseModel
import openai
from pptx import Presentation
import os

# Initialize FastAPI app
app = FastAPI()

# Request Model for API
class PresentationRequest(BaseModel):
    topic: str
    num_slides: int

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/generate_ppt")
def generate_ppt(request: PresentationRequest):
    prs = Presentation()
    
    for i in range(request.num_slides):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": f"Generate slide {i+1} on {request.topic}"}]
        )
        slide_content = response["choices"][0]["message"]["content"]
        
        slide = prs.slides.add_slide(prs.slide_layouts[5])
        title = slide.shapes.title
        title.text = slide_content

    prs.save("output.pptx")
    return {"message": "Presentation created successfully", "file": "output.pptx"}
