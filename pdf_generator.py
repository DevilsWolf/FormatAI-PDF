# pdf_generator.py

import os
import re
import traceback # Import traceback for detailed errors

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4 
from reportlab.lib.enums import TA_LEFT

from config import (
    PDF_FONT_NAME_DEFAULT, 
    PDF_FONT_SIZE_DEFAULT,  
    PDF_PARAGRAPH_SPACE_INCHES, 
    PDF_HEADING_SPACE_AFTER_INCHES,
    PDF_BULLET_INDENT_POINTS
)

PAGE_SIZES = { 
    "Letter": letter,
    "A4": A4,
}

def generate_pdf(text, filename="output.pdf", page_size_name="Letter", font_size=PDF_FONT_SIZE_DEFAULT):
    """
    Generates a formatted PDF from a text string using ReportLab's platypus.
    Parses simple Markdown-like headings (#, ##, ###) and bullet list items (*, -).
    Lines starting with numbers (e.g., "1. Item") are treated as normal paragraphs.
    Includes enhanced error reporting.
    """
    print(f"DEBUG (pdf_generator): generate_pdf started for '{filename}' with font_size {font_size}.") # DEBUG
    
    if page_size_name not in PAGE_SIZES:
        print(f"DEBUG (pdf_generator): Unknown page size '{page_size_name}'. Using default 'Letter'.")
        page_size_name = "Letter"

    current_page_size = PAGE_SIZES[page_size_name]
    
    # --- Ensure filename path exists (ReportLab doesn't create directories) ---
    output_dir = os.path.dirname(filename)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"DEBUG (pdf_generator): Created directory '{output_dir}'")
        except Exception as e:
            error_msg = f"Failed to create directory for PDF '{output_dir}': {e}"
            print(f"ERROR (pdf_generator): {error_msg}")
            return False, error_msg
            
    doc = SimpleDocTemplate(filename, pagesize=current_page_size)
    
    try: # Wrap style definition in try block in case of font issues later
        styles = getSampleStyleSheet() 
        normal_style = ParagraphStyle( name='Normal', parent=styles['Normal'], fontName=PDF_FONT_NAME_DEFAULT, fontSize=font_size, leading=font_size * 1.2, spaceAfter=0 )
        heading1_style = ParagraphStyle( name='Heading1', parent=styles['Heading1'], fontName=PDF_FONT_NAME_DEFAULT, fontSize=font_size * 1.8, leading=font_size * 1.8 * 1.2, spaceBefore=font_size * 1.2, spaceAfter=PDF_HEADING_SPACE_AFTER_INCHES * inch, keepWithNext=True )
        heading2_style = ParagraphStyle( name='Heading2', parent=styles['Heading2'], fontName=PDF_FONT_NAME_DEFAULT, fontSize=font_size * 1.4, leading=font_size * 1.4 * 1.2, spaceBefore=font_size * 1.0, spaceAfter=PDF_HEADING_SPACE_AFTER_INCHES * inch * 0.75, keepWithNext=True )
        heading3_style = ParagraphStyle( name='Heading3', parent=styles['Heading3'], fontName=PDF_FONT_NAME_DEFAULT, fontSize=font_size * 1.2, leading=font_size * 1.2 * 1.2, spaceBefore=font_size * 0.8, spaceAfter=PDF_HEADING_SPACE_AFTER_INCHES * inch * 0.5, keepWithNext=True )
        list_item_paragraph_style = ParagraphStyle( name='ListItemParagraph', parent=normal_style, spaceBefore=0, spaceAfter=0, leftIndent=0, firstLineIndent=0, bulletIndent=0, alignment=TA_LEFT )
    except Exception as e:
        error_msg = f"Error setting up ReportLab styles (check font '{PDF_FONT_NAME_DEFAULT}?): {e}"
        print(f"ERROR (pdf_generator): {error_msg}")
        return False, error_msg

    story = []
    lines = text.strip().split('\n')
    paragraph_buffer = []
    current_bullet_list_items = [] 

    # --- Helper Functions (No changes needed here) ---
    def add_paragraph_buffer_to_story():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            para_text = " ".join(paragraph_buffer).strip()
            if para_text:
                try: story.append(Paragraph(para_text, normal_style))
                except Exception as e: print(f"WARNING (pdf_generator): Skipping paragraph due to error: {e}. Text: '{para_text[:100]}...'"); # Skip bad paras
                story.append(Spacer(1, PDF_PARAGRAPH_SPACE_INCHES * inch))
            paragraph_buffer = []
    def add_bullet_list_to_story(): 
        nonlocal current_bullet_list_items
        if current_bullet_list_items:
            list_elements = []
            for item_text in current_bullet_list_items:
                try: p_item = Paragraph(item_text, list_item_paragraph_style)
                except Exception as e: print(f"WARNING (pdf_generator): Skipping list item due to error: {e}. Text: '{item_text[:100]}...'"); continue # Skip bad items
                list_elements.append(ListItem(p_item))
            if list_elements: # Only add if there are valid elements
                list_flowable = ListFlowable( list_elements, bulletType='bullet', bulletText='•', leftIndent=PDF_BULLET_INDENT_POINTS, )
                story.append(list_flowable)
                story.append(Spacer(1, PDF_PARAGRAPH_SPACE_INCHES * inch * 0.5))
            current_bullet_list_items = []

    # --- Parsing Loop ---        
    for line_idx, line in enumerate(lines):
        # print(f"DEBUG (pdf_generator): Processing line {line_idx}: '{line[:80]}...'") # Optional: Very verbose debug
        cleaned_line = line.strip()
        next_line_is_bullet_item = False
        if line_idx + 1 < len(lines):
            next_cleaned_line = lines[line_idx+1].strip()
            if next_cleaned_line.startswith(('* ', '- ')): next_line_is_bullet_item = True
        if not cleaned_line.startswith(('* ', '- ')) and current_bullet_list_items: add_bullet_list_to_story()

        try: # Wrap parsing actions in try block to catch errors related to content
            if cleaned_line.startswith('# '):
                add_paragraph_buffer_to_story(); add_bullet_list_to_story() 
                heading_text = cleaned_line[2:].strip()
                if heading_text: story.append(Paragraph(heading_text, heading1_style))
                continue
            if cleaned_line.startswith('## '):
                add_paragraph_buffer_to_story(); add_bullet_list_to_story()
                heading_text = cleaned_line[3:].strip()
                if heading_text: story.append(Paragraph(heading_text, heading2_style))
                continue
            if cleaned_line.startswith('### '):
                add_paragraph_buffer_to_story(); add_bullet_list_to_story()
                heading_text = cleaned_line[4:].strip()
                if heading_text: story.append(Paragraph(heading_text, heading3_style))
                continue

            if cleaned_line.startswith(('* ', '- ')):
                add_paragraph_buffer_to_story() 
                bullet_text = cleaned_line[2:].strip()
                if bullet_text: current_bullet_list_items.append(bullet_text)
                if not next_line_is_bullet_item: add_bullet_list_to_story()
                continue
                
            if cleaned_line == "": add_paragraph_buffer_to_story()
            else: paragraph_buffer.append(line) 
        except Exception as e:
             print(f"WARNING (pdf_generator): Error processing line {line_idx+1} ('{line[:80]}...'): {e}. Skipping effects of this line.")
             # Optionally clear buffers if error occurs?
             paragraph_buffer = [] 
             current_bullet_list_items = []

    # --- Final cleanup ---
    try:
        add_paragraph_buffer_to_story()
        add_bullet_list_to_story() 
    except Exception as e:
        print(f"WARNING (pdf_generator): Error during final buffer cleanup: {e}")


    if not story:
        story.append(Paragraph("The processed text was empty or resulted in no valid PDF content.", normal_style))
        print("DEBUG (pdf_generator): Story was empty, added default paragraph.") 
    
    print(f"DEBUG (pdf_generator): Attempting doc.build(story) with {len(story)} flowables...") 
    
    # --- Build Phase ---
    try:
        doc.build(story)
        print(f"DEBUG (pdf_generator): doc.build successful for '{filename}'") 
        return True, f"PDF successfully created: {os.path.basename(filename)}"
    except Exception as e:
        # --- More Detailed Error Reporting ---
        error_details = traceback.format_exc() 
        full_error_msg = f"Error creating PDF (ReportLab doc.build failed for '{filename}'): {e}\nDetails:\n{error_details}"
        print(f"ERROR (pdf_generator): {full_error_msg}") 
        # Try to provide a snippet of the story around where it might have failed (advanced)
        # story_repr = [repr(f)[:100] + ('...' if len(repr(f)) > 100 else '') for f in story]
        # print(f"DEBUG (pdf_generator): Story content (first/last few items):\n{story_repr[:5]}\n...\n{story_repr[-5:]}")
        return False, f"Error creating PDF (ReportLab build failed): {e}" # Return simpler message to UI


# --- Standalone Test ---
if __name__ == '__main__':
    # ... (standalone test code remains the same) ...
    print("Running PDF generator standalone test...")
    sample_formatted_text = """# Title\n\nPara 1.\n\n* Item 1\n* Item 2 with <b>bold</b>\n\n## H2\n\nPara 2."""
    output_file = "standalone_pdf_test_debug.pdf"
    success, message = generate_pdf(sample_formatted_text, output_file, page_size_name="A4", font_size=11)
    print(message)