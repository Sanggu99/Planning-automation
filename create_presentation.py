
import sys
import json
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation(data_file, output_file):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    prs = Presentation()

    # Helper to clean up text
    def add_bullet(tf, text, level=0):
        p = tf.add_paragraph()
        p.text = text
        p.level = level

    # 1. Title Slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = data.get("project_name", "Project Name")
    slide.placeholders[1].text = data.get("subtitle", "")

    # 2. Project Overview
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "1. Project Overview"
    tf = slide.placeholders[1].text_frame
    for k, v in data.get("overview", {}).items():
        add_bullet(tf, f"{k}: {v}")

    # 3. Analysis Process (History)
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "2. Analysis Workflow Steps"
    tf = slide.placeholders[1].text_frame
    for item in data.get("history_summary", []):
        add_bullet(tf, item)

    # 4. Key Analysis Points
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "3. Key Analysis Results"
    tf = slide.placeholders[1].text_frame
    for point in data.get("analysis_points", []):
        add_bullet(tf, point)

    # 5. Masterplan Concept & Simulation
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title Only
    slide.shapes.title.text = "4. Masterplan Simulation"
    
    img_path = data.get("masterplan_image", "")
    # Check if relative path needs adjustment
    if not os.path.exists(img_path):
        # try checking relative to script? or absolute
        pass

    if img_path and os.path.exists(img_path):
        # Image on left
        slide.shapes.add_picture(img_path, Inches(0.5), Inches(1.8), height=Inches(5))
        
        # Text on right
        txBox = slide.shapes.add_textbox(Inches(6), Inches(1.8), Inches(3.5), Inches(5))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        concept_text = data.get("concept_text", "Concept details...")
        p = tf.add_paragraph()
        p.text = concept_text
        p.font.size = Pt(14)
    else:
        # Fallback if no image
        print(f"Warning: Image file not found at: {img_path}")
        txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4))
        tf = txBox.text_frame
        p = tf.add_paragraph()
        p.text = "Image not found: " + img_path
        
        # Add concept text anyway
        p2 = tf.add_paragraph()
        p2.text = data.get("concept_text", "")

    # 6. Architectural Outline
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "5. Architectural Outline"
    tf = slide.placeholders[1].text_frame
    for k, v in data.get("architectural_outline", {}).items():
        add_bullet(tf, f"{k}: {v}")

    # 7. Strategic Approach
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "6. Development Strategies"
    tf = slide.placeholders[1].text_frame
    for strategy in data.get("strategies", []):
        add_bullet(tf, strategy)

    # 8. Conclusion
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "7. Conclusion"
    tf = slide.placeholders[1].text_frame
    tf.add_paragraph().text = data.get("conclusion", "")

    # Save
    try:
        prs.save(output_file)
        print(f"Presentation saved to {output_file}")
    except Exception as e:
        print(f"Error saving: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python create_presentation.py <data_json> <output_pptx>")
    else:
        create_presentation(sys.argv[1], sys.argv[2])
