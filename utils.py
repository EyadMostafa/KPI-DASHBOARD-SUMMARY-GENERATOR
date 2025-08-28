import streamlit as st
import base64
from PIL import Image
from io import BytesIO

def image_to_base64(image_file):
    """Converts an uploaded image file to a base64 encoded string."""
    try:
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