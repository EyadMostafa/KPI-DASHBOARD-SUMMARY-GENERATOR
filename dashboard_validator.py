"""
Dashboard Image Validation Module

This module contains functions to validate if uploaded images are actually
business dashboards before processing them for analysis.
"""

import streamlit as st
import os
from llm_service import gemini_inference, ollama_inference


def validate_dashboard_image(image, model_choice):
    """
    Validate if the uploaded image is actually a dashboard using AI.
    
    Args:
        image: PIL Image object
        model_choice: String indicating which model to use ("Gemini (Online)" or "Ollama (Local)")
    
    Returns:
        bool: True if it's a dashboard, False otherwise
    """
    try:
        validation_prompt = """
Please analyze this image and determine if it is a business dashboard, KPI dashboard, or data visualization dashboard.

Look for these characteristics:
- Charts, graphs, or data visualizations
- Numbers, metrics, or KPIs
- Business-related data (sales, revenue, employees, etc.)
- Dashboard-like layout with multiple data points
- Tables, bar charts, pie charts, line graphs
- Business intelligence or analytics interface

Respond with ONLY one word:
- "YES" if this is clearly a business/dashboard image
- "NO" if this is not a dashboard (e.g., photos, random images, documents, etc.)

Be strict - only business dashboards and data visualizations should get "YES".
"""
        
        if model_choice == "Gemini (Online)":
            result = gemini_inference(validation_prompt, [image])
        else:
            result = ollama_inference(os.getenv("OLLAMA_MODEL_NAME"), validation_prompt, [image])
        
        if result:
            # Clean the response and check for YES/NO
            result_clean = result.strip().upper()
            return "YES" in result_clean and "NO" not in result_clean
        return False
        
    except Exception as e:
        st.error(f"Error validating image: {e}")
        return False


def validate_multiple_dashboards(images, model_choice):
    """
    Validate multiple dashboard images at once.
    
    Args:
        images: List of PIL Image objects
        model_choice: String indicating which model to use
    
    Returns:
        tuple: (all_valid, validation_results)
            - all_valid: bool indicating if all images are valid dashboards
            - validation_results: list of validation results for each image
    """
    validation_results = []
    
    for i, image in enumerate(images):
        is_valid = validate_dashboard_image(image, model_choice)
        validation_results.append(is_valid)
    
    all_valid = all(validation_results)
    return all_valid, validation_results


def get_validation_error_message(image_index=None):
    """
    Get a standardized error message for invalid dashboard images.
    
    Args:
        image_index: Optional index number for multiple images (e.g., "Dashboard 1", "Dashboard 2")
    
    Returns:
        str: Formatted error message
    """
    prefix = f"❌ **{image_index}** doesn't appear to be a dashboard image!" if image_index else "❌ **This doesn't appear to be a dashboard image!**"
    
    return f"""
    {prefix}
    
    Please upload an image that contains:
    - Business dashboards or KPI reports
    - Charts, graphs, or data visualizations
    - Business metrics and analytics
    
    The system detected this is not a dashboard image and cannot analyze it.
    """


def get_uploader_help_text():
    """
    Get standardized help text for file uploaders.
    
    Returns:
        str: Help text for dashboard image uploaders
    """
    return "⚠️ Only upload business dashboards, KPI reports, or data visualizations. The system will validate the image before analysis."


def validate_and_show_error(image, model_choice, image_name="This image"):
    """
    Validate an image and show error if invalid.
    
    Args:
        image: PIL Image object
        model_choice: String indicating which model to use
        image_name: Name to display in error message
    
    Returns:
        bool: True if valid, False if invalid (and shows error)
    """
    is_dashboard = validate_dashboard_image(image, model_choice)
    
    if not is_dashboard:
        error_message = get_validation_error_message(image_name)
        st.error(error_message)
        return False
    
    return True
