import streamlit as st
import ollama
import base64
import tempfile
import os
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def image_to_base64(image_file):
    """Converts an uploaded image file to a base64 encoded string."""
    try:
        # Convert PIL Image to base64
        if hasattr(image_file, 'mode'):
            img = image_file
        else:
            img = Image.open(image_file)
            
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

def ollama_inference(model_name, instruction, images_base64):
    """
    Performs inference using a multimodal Ollama model.
    """
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    'role': 'user',
                    'content': instruction,
                    'images': images_base64,
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"An error occurred during inference: {e}"

def check_model_availability(model_name):
    """Check if the Ollama model is available."""
    try:
        ollama.show(model_name)
        return True
    except Exception:
        return False

def create_pdf_report(dashboard_objective, analysis_result, filename):
    """Create a PDF report with I-Score branding and professional formatting."""
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import PageTemplate, Frame, BaseDocTemplate
    from reportlab.lib.pagesizes import letter
    
    buffer = BytesIO()
    
    # Custom page template with logo
    class LogoPageTemplate(PageTemplate):
        def __init__(self, id, frames, pagesize=letter):
            PageTemplate.__init__(self, id, frames, pagesize=pagesize)
            
        def beforeDrawPage(self, canvas, doc):
            """Add logo to every page"""
            try:
                # Professional header with I-Score branding
                # Logo area background
                canvas.setFillColor(HexColor('#F8F9FA'))  # Light background
                canvas.rect(40, letter[1] - 65, letter[0] - 80, 55, fill=1, stroke=0)
                
                # I-Score logo text with professional styling
                canvas.setFillColor(HexColor('#4F3C8F'))  # I-Score purple
                canvas.setFont("Helvetica-Bold", 18)
                canvas.drawString(50, letter[1] - 30, "I-SCORE")
                
                # Subtitle
                canvas.setFont("Helvetica", 12)
                canvas.setFillColor(HexColor('#45BCC3'))  # I-Score teal
                canvas.drawString(50, letter[1] - 48, "KPI Dashboard Analysis Report")
                
                # Add I-Score brand elements - decorative shapes
                # Teal accent rectangle
                canvas.setFillColor(HexColor('#45BCC3'))
                canvas.rect(letter[0] - 120, letter[1] - 45, 60, 8, fill=1, stroke=0)
                
                # Purple accent rectangle
                canvas.setFillColor(HexColor('#4F3C8F'))
                canvas.rect(letter[0] - 120, letter[1] - 35, 60, 4, fill=1, stroke=0)
                
                # Bottom border line
                canvas.setStrokeColor(HexColor('#45BCC3'))
                canvas.setLineWidth(3)
                canvas.line(40, letter[1] - 68, letter[0] - 40, letter[1] - 68)
                
                # Add page number at top right
                canvas.setFillColor(HexColor('#495057'))
                canvas.setFont("Helvetica", 10)
                page_num = canvas.getPageNumber()
                canvas.drawRightString(letter[0] - 50, letter[1] - 25, f"Page {page_num}")
                
            except Exception as e:
                # Fallback header if anything fails
                canvas.setFillColor(HexColor('#4F3C8F'))
                canvas.setFont("Helvetica-Bold", 16)
                canvas.drawString(50, letter[1] - 30, "I-SCORE KPI Dashboard Analyzer")
                
                # Simple line
                canvas.setStrokeColor(HexColor('#45BCC3'))
                canvas.setLineWidth(2)
                canvas.line(50, letter[1] - 40, letter[0] - 50, letter[1] - 40)
    
    # Create document with custom page template
    doc = BaseDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,  # 1 inch
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define frame for content (below the logo area)
    frame = Frame(
        72, 72, letter[0] - 144, letter[1] - 144,  # Adjusted for 1 inch margins
        leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0
    )
    
    # Add page template
    doc.addPageTemplates([LogoPageTemplate(id='logo_template', frames=[frame])])
    
    styles = getSampleStyleSheet()
    story = []
    
    # I-Score brand colors
    iscore_teal = HexColor('#45BCC3')
    iscore_purple = HexColor('#4F3C8F')
    iscore_dark_charcoal = HexColor('#4B4947')
    iscore_gray = HexColor('#495057')
    
    # Custom styles as per specifications
    title_style = ParagraphStyle(
        'IScorerTitle',
        parent=styles['Title'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=iscore_purple,
        spaceAfter=24,
        spaceBefore=0,
        alignment=1,  # Centered
        letterSpacing=0.3,
        lineHeight=20
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=iscore_purple,
        spaceBefore=20,
        spaceAfter=12,
        leftIndent=0,
        alignment=0  # Left-aligned
    )
    
    sub_heading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Heading2'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=iscore_teal,
        spaceBefore=12,
        spaceAfter=6,
        leftIndent=0,
        alignment=0
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica',
        textColor=iscore_dark_charcoal,
        spaceBefore=4,
        spaceAfter=6,
        leftIndent=12,
        lineHeight=16,
        alignment=4  # Justified
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica',
        textColor=iscore_dark_charcoal,
        spaceBefore=3,
        spaceAfter=6,
        leftIndent=24,
        bulletIndent=12,
        lineHeight=16,
        alignment=4
    )
    
    objective_style = ParagraphStyle(
        'Objective',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Oblique',
        textColor=iscore_dark_charcoal,
        spaceBefore=8,
        spaceAfter=12,
        leftIndent=12,
        rightIndent=12,
        lineHeight=16,
        borderWidth=1,
        borderColor=iscore_teal,
        borderPadding=15,
        backColor=HexColor('#F8F9FA'),
        alignment=4
    )
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=iscore_gray,
        alignment=1,  # Centered
        spaceBefore=16,
        spaceAfter=4,
        lineHeight=12
    )
    
    # Title
    story.append(Paragraph("I-SCORE KPI Dashboard Analysis Report", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Dashboard Objective Section
    story.append(Paragraph("1. Dashboard Objective", section_heading_style))
    story.append(Paragraph(dashboard_objective, objective_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # AI Analysis Results Section
    story.append(Paragraph("2. AI Analysis Results", section_heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    # Process analysis results with refined parsing
    def clean_markdown(text):
        import re
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        return text.strip()
    
    analysis_lines = analysis_result.split('\n')
    
    for line in analysis_lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        
        # Main sub-sections (a. Overall Summary)
        if line.startswith(tuple(f'{chr(97+i)}. ' for i in range(26))):
            clean_line = clean_markdown(line)
            story.append(Paragraph(clean_line, sub_heading_style))
        
        # Numbered list items (1. Total Employees:)
        elif line.startswith(tuple(f'{i}. ' for i in range(1, 10))):
            clean_line = clean_markdown(line)
            if ':' in clean_line:
                parts = clean_line.split(':', 1)
                title = parts[0].strip()
                description = parts[1].strip() if len(parts) > 1 else ''
                formatted = f'<b>{title}:</b><br />{description}'
                story.append(Paragraph(formatted, body_style))
            else:
                story.append(Paragraph(clean_line, body_style))
        
        # Bullet points
        elif line.startswith(('*', '-', '•')):
            clean_line = clean_markdown(line.lstrip('*-• ').strip())
            story.append(Paragraph(f'• {clean_line}', bullet_style))
        
        # Regular paragraphs
        else:
            clean_line = clean_markdown(line)
            if clean_line:
                story.append(Paragraph(clean_line, body_style))
    
    # Footer
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Generated by I-Score KPI Dashboard Analyzer | Powered by Ollama Qwen 2.5 Vision Model", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def main():
    # Read the SVG logo content
    try:
        with open("JPG to SVG Conversion.svg", "r", encoding="utf-8") as f:
            svg_logo = f.read()
    except FileNotFoundError:
        svg_logo = ""
        print("Warning: SVG logo file not found")
    
    st.set_page_config(
        page_title="KPI Dashboard Analyzer",
        page_icon="data:image/svg+xml;base64," + base64.b64encode(svg_logo.encode('utf-8')).decode('utf-8') if svg_logo else "📊",
        layout="wide"
    )
    
    # Custom CSS with I-Score logo theme - Complete Brand Integration
    st.markdown("""
    <style>
    /* Import Google Fonts matching I-Score's modern aesthetic */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* I-Score Logo Color Palette - Exact Brand Colors */
    :root {
        /* Primary brand colors from logo */
        --iscore-teal-primary: #45BCC3;
        --iscore-purple-primary: #4F3C8F;
        --iscore-dark-charcoal: #4B4947;
        
        /* Secondary variations inspired by logo elements */
        --iscore-teal-light: #6BCFD4;
        --iscore-teal-dark: #2E9BA3;
        --iscore-purple-light: #6B52B8;
        --iscore-purple-dark: #3D2D6F;
        
        /* Neutral colors maintaining logo's sophistication */
        --iscore-gray-100: #F8F9FA;
        --iscore-gray-200: #E9ECEF;
        --iscore-gray-300: #DEE2E6;
        --iscore-gray-800: #495057;
        
        /* Alpha variations for depth and layering */
        --iscore-teal-alpha-05: rgba(69, 188, 195, 0.05);
        --iscore-teal-alpha-10: rgba(69, 188, 195, 0.1);
        --iscore-teal-alpha-15: rgba(69, 188, 195, 0.15);
        --iscore-teal-alpha-20: rgba(69, 188, 195, 0.2);
        --iscore-teal-alpha-30: rgba(69, 188, 195, 0.3);
        --iscore-purple-alpha-05: rgba(79, 60, 143, 0.05);
        --iscore-purple-alpha-10: rgba(79, 60, 143, 0.1);
        --iscore-purple-alpha-15: rgba(79, 60, 143, 0.15);
        --iscore-purple-alpha-20: rgba(79, 60, 143, 0.2);
        --iscore-purple-alpha-30: rgba(79, 60, 143, 0.3);
        
        /* Logo-inspired gradients */
        --iscore-gradient-primary: linear-gradient(135deg, var(--iscore-teal-primary) 0%, var(--iscore-purple-primary) 100%);
        --iscore-gradient-light: linear-gradient(135deg, var(--iscore-teal-light) 0%, var(--iscore-purple-light) 100%);
        --iscore-gradient-subtle: linear-gradient(145deg, var(--iscore-teal-alpha-10) 0%, var(--iscore-purple-alpha-10) 100%);
    }
    
    /* Global styling reflecting I-Score's clean, modern aesthetic */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: var(--iscore-gray-100);
        color: var(--iscore-dark-charcoal);
    }
    
    /* Header with I-Score logo-inspired design */
    .main-header {
        background: var(--iscore-gradient-primary);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        text-align: center;
        box-shadow: 
            0 10px 40px var(--iscore-teal-alpha-30),
            0 20px 80px var(--iscore-purple-alpha-20);
        position: relative;
        overflow: hidden;
    }
    
    /* Add subtle pattern overlay mimicking logo's sophistication */
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, var(--iscore-teal-light) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, var(--iscore-purple-light) 0%, transparent 50%);
        opacity: 0.1;
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.8rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .main-header h3 {
        color: rgba(255, 255, 255, 0.9) !important;
        margin-bottom: 0.8rem;
        font-weight: 500;
        font-size: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 400;
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    
    /* Typography system inspired by I-Score's clean design */
    h1, h2, h3, h4, h5, h6 {
        color: var(--iscore-purple-primary) !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }
    
    /* Section headers with I-Score branding elements */
    .section-header {
        color: var(--iscore-purple-primary) !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid var(--iscore-teal-primary);
        display: inline-block;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 30%;
        height: 3px;
        background: var(--iscore-purple-primary);
        border-radius: 1px;
    }
    
    /* Primary buttons inspired by I-Score logo's modern aesthetic */
    .stButton > button {
        background: var(--iscore-gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.02em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 25px var(--iscore-teal-alpha-30),
            0 4px 10px var(--iscore-purple-alpha-20) !important;
        text-transform: none !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: var(--iscore-gradient-light);
        transition: left 0.4s ease;
        z-index: -1;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 12px 35px var(--iscore-teal-alpha-30),
            0 8px 20px var(--iscore-purple-alpha-30) !important;
    }
    
    .stButton > button:hover::before {
        left: 0;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.01) !important;
    }
    
    /* File uploader with I-Score styling inspiration */
    .stFileUploader > div > div {
        border: 3px dashed var(--iscore-teal-primary) !important;
        border-radius: 20px !important;
        background: var(--iscore-gradient-subtle) !important;
        padding: 2.5rem !important;
        text-align: center !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stFileUploader > div > div::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, var(--iscore-teal-alpha-10) 0%, transparent 70%);
        transform: translate(-50%, -50%);
        pointer-events: none;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--iscore-purple-primary) !important;
        background: linear-gradient(145deg, var(--iscore-teal-alpha-20), var(--iscore-purple-alpha-10)) !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 10px 30px var(--iscore-teal-alpha-20) !important;
    }
    
    .stFileUploader label {
        color: var(--iscore-purple-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Text area with I-Score brand consistency */
    .stTextArea > div > div > textarea {
        border: 2px solid var(--iscore-teal-primary) !important;
        border-radius: 16px !important;
        background: var(--iscore-gradient-subtle) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
        color: var(--iscore-dark-charcoal) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: vertical !important;
        padding: 1rem !important;
    }
    
    .stTextArea > div > div > textarea:hover {
        border-color: var(--iscore-purple-primary) !important;
        background: linear-gradient(145deg, var(--iscore-teal-alpha-10), var(--iscore-purple-alpha-05)) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px var(--iscore-teal-alpha-20) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--iscore-purple-primary) !important;
        box-shadow: 
            0 0 0 3px var(--iscore-purple-alpha-20),
            0 8px 25px var(--iscore-teal-alpha-20) !important;
        background: white !important;
        transform: scale(1.01) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--iscore-gray-800) !important;
        opacity: 0.7 !important;
    }
    
    .stTextArea label {
        color: var(--iscore-purple-primary) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Tab navigation with I-Score design language */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        border-bottom: 2px solid var(--iscore-gray-200);
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--iscore-gradient-subtle) !important;
        color: var(--iscore-purple-primary) !important;
        border-radius: 16px 16px 0 0 !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        border: 2px solid var(--iscore-teal-alpha-20) !important;
        border-bottom: none !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 1rem 2rem !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: var(--iscore-gradient-light);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-20), var(--iscore-purple-alpha-15)) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px var(--iscore-teal-alpha-20) !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        opacity: 0.1;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--iscore-gradient-primary) !important;
        color: white !important;
        border-color: var(--iscore-teal-primary) !important;
        box-shadow: 0 8px 25px var(--iscore-teal-alpha-30) !important;
        transform: translateY(-1px) !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background: white !important;
        border-radius: 0 20px 20px 20px !important;
        padding: 2.5rem !important;
        box-shadow: 
            0 8px 30px var(--iscore-teal-alpha-20),
            0 4px 15px var(--iscore-purple-alpha-10) !important;
        border: 2px solid var(--iscore-teal-alpha-20) !important;
        border-top: none !important;
        margin-top: -2px !important;
    }
    
    /* Alert components styled with I-Score branding */
    .stInfo {
        background: var(--iscore-gradient-subtle) !important;
        border: 2px solid var(--iscore-teal-primary) !important;
        border-left: 6px solid var(--iscore-teal-primary) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 15px var(--iscore-teal-alpha-20) !important;
    }
    
    .stSuccess {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-20), var(--iscore-teal-alpha-10)) !important;
        border: 2px solid var(--iscore-teal-primary) !important;
        border-left: 6px solid var(--iscore-teal-primary) !important;
        border-radius: 12px !important;
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 15px var(--iscore-teal-alpha-20) !important;
        padding: 1.5rem !important;
    }
    
    .stError {
        background: linear-gradient(145deg, var(--iscore-purple-alpha-10), var(--iscore-purple-alpha-10)) !important;
        border: 2px solid var(--iscore-purple-primary) !important;
        border-left: 6px solid var(--iscore-purple-primary) !important;
        border-radius: 12px !important;
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 15px var(--iscore-purple-alpha-20) !important;
        padding: 1.5rem !important;
    }
    
    .stWarning {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-10), var(--iscore-teal-alpha-10)) !important;
        border: 2px solid var(--iscore-teal-dark) !important;
        border-left: 6px solid var(--iscore-teal-dark) !important;
        border-radius: 12px !important;
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: 0 4px 15px var(--iscore-teal-alpha-20) !important;
        padding: 1.5rem !important;
    }
    
    /* Expander styling with I-Score consistency */
    .streamlit-expanderHeader {
        background: var(--iscore-gradient-subtle) !important;
        border-radius: 12px !important;
        color: var(--iscore-purple-primary) !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        border: 2px solid var(--iscore-teal-alpha-30) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 1rem 1.5rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-20), var(--iscore-purple-alpha-15)) !important;
        border-color: var(--iscore-purple-primary) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px var(--iscore-teal-alpha-20) !important;
    }
    
    .streamlit-expanderContent {
        background: white !important;
        border-radius: 0 0 12px 12px !important;
        border: 2px solid var(--iscore-teal-alpha-20) !important;
        border-top: none !important;
        margin-top: -2px !important;
        box-shadow: 0 4px 15px var(--iscore-teal-alpha-10) !important;
    }
    
    /* Download button with premium I-Score styling */
    .stDownloadButton > button {
        background: var(--iscore-gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: 0.02em !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            0 8px 25px var(--iscore-teal-alpha-30),
            0 4px 15px var(--iscore-purple-alpha-20) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stDownloadButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: var(--iscore-gradient-light);
        transition: left 0.4s ease;
        z-index: -1;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 
            0 12px 35px var(--iscore-teal-alpha-30),
            0 8px 20px var(--iscore-purple-alpha-30) !important;
    }
    
    .stDownloadButton > button:hover::before {
        left: 0;
    }
    
    /* Image display styling */
    .stImage > div {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 15px rgba(69, 188, 195, 0.2) !important;
        border: 2px solid rgba(69, 188, 195, 0.3) !important;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #45BCC3 !important;
        border-right-color: #4F3C8F !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #45BCC3 0%, #4F3C8F 100%) !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border: 2px solid #45BCC3 !important;
        border-radius: 10px !important;
        background: linear-gradient(145deg, rgba(69, 188, 195, 0.02), rgba(79, 60, 143, 0.02)) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #4F3C8F !important;
        box-shadow: 0 0 0 2px rgba(79, 60, 143, 0.2) !important;
    }
    
    /* Markdown content styling */
    .stMarkdown {
        color: #4B4947 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Columns styling */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Footer with I-Score brand consistency */
    .footer-text {
        text-align: center;
        color: var(--iscore-dark-charcoal);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        font-size: 1rem;
        padding: 3rem 0;
        border-top: 2px solid var(--iscore-teal-alpha-30);
        margin-top: 4rem;
        background: var(--iscore-gradient-subtle);
        position: relative;
    }
    
    .footer-text::before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 2px;
        background: var(--iscore-gradient-primary);
    }
    
    /* Custom scrollbar reflecting I-Score aesthetic */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--iscore-gray-200);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--iscore-gradient-primary);
        border-radius: 6px;
        border: 2px solid var(--iscore-gray-200);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--iscore-gradient-light);
    }
    
    /* Additional polish for modern web aesthetics */
    .stMarkdown {
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
    }
    
    /* Override any remaining default red/orange hover effects */
    input:hover, textarea:hover, select:hover {
        border-color: var(--iscore-purple-primary) !important;
        outline: none !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: var(--iscore-purple-primary) !important;
        outline: none !important;
        box-shadow: 0 0 0 2px var(--iscore-purple-alpha-20) !important;
    }
    
    /* File uploader drag and drop hover states */
    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--iscore-purple-primary) !important;
        background: var(--iscore-gradient-subtle) !important;
    }
    
    /* General hover states for interactive elements */
    [role="button"]:hover {
        background-color: var(--iscore-teal-alpha-10) !important;
    }
    
    /* Enhanced image styling */
    .stImage > div {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 
            0 8px 30px var(--iscore-teal-alpha-20),
            0 4px 15px var(--iscore-purple-alpha-10) !important;
        border: 3px solid var(--iscore-teal-alpha-30) !important;
        transition: transform 0.3s ease !important;
    }
    
    .stImage > div:hover {
        transform: scale(1.02) !important;
    }
    
    /* Spinner with I-Score branding */
    .stSpinner > div {
        border-top-color: var(--iscore-teal-primary) !important;
        border-right-color: var(--iscore-purple-primary) !important;
        border-bottom-color: var(--iscore-teal-light) !important;
        border-left-color: var(--iscore-purple-light) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: var(--iscore-gradient-primary) !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1>📊 KPI Dashboard Analyzer</h1>
        <h3>AI-Powered Dashboard Analysis and Insights</h3>
        <p>Upload your KPI dashboard image and provide the business objective to get detailed analysis and strategic recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fixed model configuration
    model_name = "qwen2.5vl:7b"
    
    # Check model availability
    if not check_model_availability(model_name):
        st.error(f"❌ Model '{model_name}' not found. Please pull it using: `ollama pull {model_name}`")
        st.stop()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Dashboard")
        uploaded_file = st.file_uploader(
            "Choose a KPI dashboard image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload your KPI dashboard image (PNG, JPG, or JPEG format)"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Dashboard", use_container_width=True)
            
            # Image details
            st.info(f"**File:** {uploaded_file.name}\n**Size:** {image.size}\n**Mode:** {image.mode}")
    
    with col2:
        st.header("🎯 Dashboard Objective")
        dashboard_objective = st.text_area(
            "Enter the business objective for this dashboard",
            placeholder="e.g., To monitor and analyze the company's employee distribution and headcount across different departments and locations to support strategic workforce planning and talent management.",
            height=150,
            help="Describe the primary business goal or purpose of this dashboard"
        )
        
        # Example objectives
        with st.expander("💡 Example Objectives"):
            st.markdown("""
            **HR Dashboard:**
            To monitor employee distribution and performance metrics to support workforce planning and talent management.
            
            **Sales Dashboard:**
            To track revenue performance, customer acquisition, and sales team productivity to drive business growth.
            
            **Financial Dashboard:**
            To monitor key financial metrics including revenue, expenses, and profitability to ensure fiscal health.
            """)
    
    # Initialize session state for storing analysis results
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'analysis_objective' not in st.session_state:
        st.session_state.analysis_objective = None
    if 'analysis_image' not in st.session_state:
        st.session_state.analysis_image = None
    if 'analysis_filename' not in st.session_state:
        st.session_state.analysis_filename = None

    # Analysis section
    st.header("🔍 Analysis")
    
    # Show analyze button if image is uploaded and objective has any text
    if uploaded_file is not None and len(dashboard_objective.strip()) > 0:
        if st.button("🚀 Analyze Dashboard", type="primary", use_container_width=True):
            with st.spinner("Analyzing dashboard... This may take a few moments."):
                # Convert image to base64
                image_b64 = image_to_base64(image)
                
                if image_b64:
                    # Create the prompt
                    prompt_template = """
As an expert data analyst, your task is to generate a concise summary of the provided KPI dashboard. The primary business objective for this dashboard is:
"{objective}"

Based on the dashboard image and the stated objective, provide a summary that includes the following sections:

1.  **Overall Summary:** A brief, high-level overview of the dashboard's current status in relation to the business objective.
2.  **Key KPI Analysis:**
    *   Identify the main KPIs presented (e.g., total employees, distribution by department, gender ratio).
    *   For each KPI, describe its current value and explain its significance in the context of the objective.
    *   Highlight any notable trends or comparisons shown in the visualizations.
3.  **Core Insights and Trends:**
    *   What are the most critical insights that can be drawn from the data?
    *   Are there any significant patterns, anomalies, or correlations that stand out? (e.g., one department being significantly larger than others).
4.  **Strategic Recommendations:**
    *   Based on your analysis, provide 1-2 actionable recommendations that would help the business achieve its workforce planning and talent management goals.

Please ensure your summary is clear, data-driven, and directly tied to the provided objective to facilitate informed decision-making.
"""
                    
                    instruction = prompt_template.format(objective=dashboard_objective)
                    
                    # Perform inference
                    result = ollama_inference(model_name, instruction, [image_b64])
                    
                    # Store results in session state
                    st.session_state.analysis_result = result
                    st.session_state.analysis_objective = dashboard_objective
                    st.session_state.analysis_image = image
                    st.session_state.analysis_filename = uploaded_file.name
                    
                    # Display success message
                    st.success("✅ Analysis Complete!")
                else:
                    st.error("Failed to process the uploaded image. Please try again.")
    
    # Display analysis results if they exist in session state
    if st.session_state.analysis_result is not None:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Analysis Results", "🎯 Objective", "🖼️ Dashboard"])
        
        with tab1:
            st.markdown("### AI Analysis Results")
            st.markdown(st.session_state.analysis_result)
            
            # Download button for PDF results
            pdf_buffer = create_pdf_report(
                st.session_state.analysis_objective, 
                st.session_state.analysis_result, 
                st.session_state.analysis_filename
            )
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_buffer,
                file_name=f"dashboard_analysis_{st.session_state.analysis_filename.split('.')[0]}.pdf",
                mime="application/pdf",
                key="download_pdf"
            )
        
        with tab2:
            st.markdown("### Dashboard Objective")
            st.info(st.session_state.analysis_objective)
        
        with tab3:
            st.markdown("### Dashboard Image")
            st.image(st.session_state.analysis_image, caption="Analyzed Dashboard", use_container_width=True)
    
    elif uploaded_file is None:
        st.info("👆 Please upload a dashboard image to get started.")
    elif not dashboard_objective.strip():
        st.info("📝 Please enter the dashboard objective to proceed with analysis.")
    
    # Footer with consistent styling
    st.markdown("""
    <div class="footer-text">
        <strong>Powered by Ollama Qwen 2.5 Vision Model</strong> | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()