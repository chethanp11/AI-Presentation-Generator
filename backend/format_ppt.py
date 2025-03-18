from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx import Presentation  # ✅ FIXED: Added missing import

# ---------------------- 🎨 DESIGN CONFIGURATIONS ----------------------
DEFAULT_FONT_SIZE = Pt(22)
HEADER_FONT_SIZE = Pt(30)
BODY_FONT_SIZE = Pt(20)

HEADER_COLOR = RGBColor(0, 0, 139)  # Dark Blue for headers
CONTENT_COLOR = RGBColor(50, 50, 50)  # Dark gray for content
BACKGROUND_COLOR = RGBColor(240, 240, 255)  # Light blue background

SLIDE_WIDTH = Inches(13.33)  # Standard 16:9 aspect ratio
SLIDE_HEIGHT = Inches(7.5)

# ---------------------- 🖌️ APPLY FORMATTING FUNCTION ----------------------
def apply_formatting(prs, gpt_feedback):
    """
    Applies professional formatting to PowerPoint slides:
    - Keeps content within layout
    - Adjusts font & colors
    - Uses GPT feedback to refine formatting
    """
    for slide in prs.slides:
        # Set slide background color
        set_slide_background(slide, BACKGROUND_COLOR)

        # Format headers and content
        format_text_elements(slide)

        # Apply AI-based improvements
        if gpt_feedback:
            apply_gpt_based_tweaks(slide, gpt_feedback)

    return prs

# ---------------------- 🎨 SET SLIDE BACKGROUND ----------------------
def set_slide_background(slide, color):
    """Sets a solid color background for the slide."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

# ---------------------- 📝 FORMAT HEADERS & TEXT ----------------------
def format_text_elements(slide):
    """
    Applies formatting:
    - Adjusts font size
    - Ensures correct alignment
    - Maintains readability
    """
    title_shape = slide.shapes.title  # Get title safely

    for shape in slide.shapes:
        if shape.has_text_frame:
            text_frame = shape.text_frame

            for paragraph in text_frame.paragraphs:
                for run in paragraph.runs:
                    if shape is title_shape and title_shape is not None:
                        run.font.size = HEADER_FONT_SIZE
                        run.font.bold = True
                        run.font.color.rgb = HEADER_COLOR
                        paragraph.alignment = PP_ALIGN.CENTER
                    else:
                        run.font.size = BODY_FONT_SIZE
                        run.font.color.rgb = CONTENT_COLOR
                        paragraph.alignment = PP_ALIGN.LEFT

            # Fix text overflow
            ensure_text_fits(shape, text_frame)

# ---------------------- ✂️ FIX TEXT OVERFLOW ----------------------

def ensure_text_fits(shape, text_frame):
    """
    Ensures text fits inside the shape by dynamically reducing font size.
    """
    max_width = shape.width - Inches(0.5)  # Keep padding
    max_height = shape.height - Inches(0.5)

    for paragraph in text_frame.paragraphs:
        for run in paragraph.runs:
            text_size = run.font.size or Pt(20)  # Default font size if missing
            while shape.width > max_width or shape.height > max_height:
                text_size -= Pt(2)  # Reduce font size
                run.font.size = text_size
                if text_size < Pt(14):  # Prevent text from becoming too small
                    break
                    
# ---------------------- 🤖 APPLY GPT-DRIVEN FORMATTING TWEAKS ----------------------
def apply_gpt_based_tweaks(slide, gpt_feedback):
    """
    Uses AI-generated feedback to enhance slide design.
    - Adds bullet points for readability
    - Adjusts font size if text is too small
    - Removes unnecessary GPT-generated conversation artifacts
    """
    feedback_lower = gpt_feedback.lower()

    for shape in slide.shapes:
        if shape.has_text_frame:
            text_frame = shape.text_frame

            # Remove GPT artifacts like "Sure! Here's your slide:"
            text_frame.text = text_frame.text.replace("Sure! Here's your slide:", "").strip()

            # Apply bullet points if recommended
            if "use bullet points" in feedback_lower:
                for paragraph in text_frame.paragraphs:
                    if not paragraph.text.startswith("•"):
                        paragraph.text = f"• {paragraph.text}"

            # Increase text size if necessary
            if "text too small" in feedback_lower:
                for paragraph in text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = BODY_FONT_SIZE + Pt(4)

    return slide