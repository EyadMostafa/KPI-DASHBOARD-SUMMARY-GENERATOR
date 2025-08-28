import streamlit as st
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageTemplate, Frame, BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from io import BytesIO

def create_pdf_report(dashboard_objective, analysis_result, filename):
    """Create a PDF report with I-Score branding and professional formatting."""
    
    buffer = BytesIO()
    
    class LogoPageTemplate(PageTemplate):
        def __init__(self, id, frames, pagesize=letter):
            PageTemplate.__init__(self, id, frames, pagesize=pagesize)
            
        def beforeDrawPage(self, canvas, doc):
            try:
                canvas.setFillColor(HexColor('#F8F9FA'))
                canvas.rect(40, letter[1] - 65, letter[0] - 80, 55, fill=1, stroke=0)
                
                canvas.setFillColor(HexColor('#4F3C8F'))
                canvas.setFont("Helvetica-Bold", 18)
                canvas.drawString(50, letter[1] - 30, "I-SCORE")
                
                canvas.setFont("Helvetica", 12)
                canvas.setFillColor(HexColor('#45BCC3'))
                canvas.drawString(50, letter[1] - 48, "KPI Dashboard Analysis Report")
                
                canvas.setFillColor(HexColor('#45BCC3'))
                canvas.rect(letter[0] - 120, letter[1] - 45, 60, 8, fill=1, stroke=0)
                
                canvas.setFillColor(HexColor('#4F3C8F'))
                canvas.rect(letter[0] - 120, letter[1] - 35, 60, 4, fill=1, stroke=0)
                
                canvas.setStrokeColor(HexColor('#45BCC3'))
                canvas.setLineWidth(3)
                canvas.line(40, letter[1] - 68, letter[0] - 40, letter[1] - 68)
                
                canvas.setFillColor(HexColor('#495057'))
                canvas.setFont("Helvetica", 10)
                page_num = canvas.getPageNumber()
                canvas.drawRightString(letter[0] - 50, letter[1] - 25, f"Page {page_num}")
                
            except Exception as e:
                canvas.setFillColor(HexColor('#4F3C8F'))
                canvas.setFont("Helvetica-Bold", 16)
                canvas.drawString(50, letter[1] - 30, "I-SCORE KPI Dashboard Analyzer")
                canvas.setStrokeColor(HexColor('#45BCC3'))
                canvas.setLineWidth(2)
                canvas.line(50, letter[1] - 40, letter[0] - 50, letter[1] - 40)
    
    doc = BaseDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    frame = Frame(
        72, 72, letter[0] - 144, letter[1] - 144,
        leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0
    )
    
    doc.addPageTemplates([LogoPageTemplate(id='logo_template', frames=[frame])])
    
    styles = getSampleStyleSheet()
    story = []
    
    iscore_teal = HexColor('#45BCC3')
    iscore_purple = HexColor('#4F3C8F')
    iscore_dark_charcoal = HexColor('#4B4947')
    iscore_gray = HexColor('#495057')
    
    title_style = ParagraphStyle(
        'IScorerTitle',
        parent=styles['Title'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=iscore_purple,
        spaceAfter=24,
        spaceBefore=0,
        alignment=1,
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
        alignment=0
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
        alignment=4
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
        alignment=1,
        spaceBefore=16,
        spaceAfter=4,
        lineHeight=12
    )
    
    story.append(Paragraph("I-SCORE KPI Dashboard Analysis Report", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph("1. Dashboard Objective", section_heading_style))
    story.append(Paragraph(dashboard_objective, objective_style))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("2. AI Analysis Results", section_heading_style))
    story.append(Spacer(1, 0.1 * inch))
    
    def clean_markdown(text):
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
        
        if line.startswith(tuple(f'{chr(97+i)}. ' for i in range(26))):
            clean_line = clean_markdown(line)
            story.append(Paragraph(clean_line, sub_heading_style))
        
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
        
        elif line.startswith(('*', '-', '•')):
            clean_line = clean_markdown(line.lstrip('*-• ').strip())
            story.append(Paragraph(f'• {clean_line}', bullet_style))
        
        else:
            clean_line = clean_markdown(line)
            if clean_line:
                story.append(Paragraph(clean_line, body_style))
    
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Generated by I-Score KPI Dashboard Analyzer | Powered by Gemini Pro Vision Model", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer