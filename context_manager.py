import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image
from utils import image_to_base64

class DashboardContextManager:
    """Minimal context manager for dashboard sessions and chat functionality."""
    
    def __init__(self):
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize basic session state structure."""
        if 'current_session' not in st.session_state:
            st.session_state.current_session = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
    
    def create_session(self, image: Image.Image, filename: str, objective: str, 
                      analysis: str, model_used: str) -> bool:
        """Create a new session with dashboard data."""
        try:
            # Convert image to base64 using existing utils function
            image_base64 = image_to_base64(image)
            if not image_base64:
                return False
            
            # Create session data
            session_data = {
                "image_base64": image_base64,
                "image_pil": image,  # Keep for display
                "filename": filename,
                "objective": objective,
                "analysis": analysis,
                "model_used": model_used,
                "created_at": datetime.now()
            }
            
            st.session_state.current_session = session_data
            st.session_state.chat_history = []  # Reset chat for new session
            
            # Update legacy state for compatibility
            st.session_state.analysis_result = analysis
            st.session_state.analysis_objective = objective
            st.session_state.analysis_image = image
            st.session_state.analysis_filename = filename
            
            return True
            
        except Exception as e:
            st.error(f"Failed to create session: {e}")
            return False
    
    def has_active_session(self) -> bool:
        """Check if there's an active session."""
        return st.session_state.current_session is not None
    
    def get_session_data(self) -> Optional[Dict]:
        """Get current session data."""
        return st.session_state.current_session
    
    def add_chat_message(self, role: str, message: str):
        """Add message to chat history."""
        chat_message = {
            "role": role,
            "message": message,
            "timestamp": datetime.now()
        }
        st.session_state.chat_history.append(chat_message)
    
    def get_chat_history(self) -> List[Dict]:
        """Get current chat history."""
        return st.session_state.chat_history
    
    def clear_chat(self):
        """Clear chat history."""
        st.session_state.chat_history = []
    
    def prepare_chat_context(self, user_message: str) -> str:
        """Prepare context for LLM chat inference."""
        if not self.has_active_session():
            return ""
        
        session = st.session_state.current_session
        
        # Format recent chat history (last 5 exchanges to keep context manageable)
        recent_chat = st.session_state.chat_history[-10:] if len(st.session_state.chat_history) > 10 else st.session_state.chat_history
        chat_context = ""
        if recent_chat:
            chat_context = "Recent conversation:\n"
            for msg in recent_chat:
                chat_context += f"{msg['role'].title()}: {msg['message']}\n"
        
        # Build complete prompt
        prompt = f"""You are analyzing a KPI dashboard. Here's the context:

            DASHBOARD OBJECTIVE: {session['objective']}
            
            INITIAL ANALYSIS:
            {session['analysis']}
            
            {chat_context}
            
            USER QUESTION: {user_message}
            
            Provide a helpful response focused on the dashboard analysis. Keep it concise and actionable."""
        
        return prompt
    
context_manager = DashboardContextManager()