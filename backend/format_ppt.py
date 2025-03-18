from pptx.util import Pt
from pptx.dml.color import RGBColor

def apply_formatting(prs):
    """Applies basic formatting to all slides in the PowerPoint presentation"""
    
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(24)  # Set font size
                        run.font.bold = True  # Make text bold
                        run.font.color.rgb = RGBColor(0, 0, 255)  # Set text color to blue

        # Set background color for all slides
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(220, 220, 220)  # Light grey background

    return prs