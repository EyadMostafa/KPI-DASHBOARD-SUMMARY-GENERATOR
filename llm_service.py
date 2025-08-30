import streamlit as st
import os
import google.generativeai as genai
import ollama
import tempfile

def gemini_inference(instruction, images_pil):
    """
    Performs analysis inference using a Gemini Vision model via API.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Gemini API key not found. Please set it in your environment.")
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt_parts = [instruction]
        if images_pil:
            for img in images_pil:
                prompt_parts.append(img)

        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return None

def ollama_inference(model_name, instruction, images_pil):
    """
    Performs analysis inference using a local Ollama model.
    """
    try:
        messages = [
            {
                'role': 'user',
                'content': instruction,
                'images': [img.filename for img in images_pil] # Note: Ollama expects image paths
            }
        ]
        
        # Save images temporarily for Ollama
        temp_dir = tempfile.mkdtemp()
        for i, img in enumerate(images_pil):
            img_path = os.path.join(temp_dir, f"image_{i}.jpg")
            img.save(img_path)
            messages[0]['images'][i] = img_path
        
        client = ollama.Client(host=os.getenv("OLLAMA_API_URL", "http://localhost:11434"))
        response = client.chat(model=model_name, messages=messages)
        
        # Clean up temporary files
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
        
        return response['message']['content']
    except Exception as e:
        st.error(f"Ollama Error: {e}")
        st.warning("Please ensure Ollama is running and the model is pulled.")
        return None
    
def gemini_chat_inference(chat_prompt):
    """
    Text-only chat inference using Gemini model.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Gemini API key not found.")
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        response = model.generate_content(chat_prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini Chat Error: {e}")
        return None

def ollama_chat_inference(model_name, chat_prompt):
    """
    Text-only chat inference using Ollama model.
    """
    try:
        client = ollama.Client(host=os.getenv("OLLAMA_API_URL", "http://localhost:11434"))
        
        messages = [{"role": "user", "content": chat_prompt}]
        response = client.chat(model=model_name, messages=messages)
        
        return response['message']['content']
    except Exception as e:
        st.error(f"Ollama Chat Error: {e}")
        return None