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
        """Initialize basic session state structure for comparison mode."""
        if 'dashboard_one' not in st.session_state:
            st.session_state.dashboard_one = None
        if 'dashboard_two' not in st.session_state:
            st.session_state.dashboard_two = None
        if 'comparison_analysis' not in st.session_state:
            st.session_state.comparison_analysis = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_session' not in st.session_state:
            st.session_state.current_session = None

    def create_session(self, dashboard_key, image, filename, objective, analysis, model_used):
        """Create a new session for a specific dashboard."""
        try:
            image_base64 = image_to_base64(image)
            if not image_base64:
                return False

            session_data = {
                "image_base64": image_base64,
                "image_pil": image,
                "filename": filename,
                "objective": objective,
                "analysis": analysis,
                "model_used": model_used,
                "created_at": datetime.now()
            }
            st.session_state[dashboard_key] = session_data
            st.session_state.current_session = dashboard_key 
            return True
        except Exception as e:
            st.error(f"Error creating session: {e}")
            return False

    def get_comparison_context(self):
        """Prepare a combined context for LLM comparison."""
        dash1 = st.session_state.dashboard_one
        dash2 = st.session_state.dashboard_two
        
        if not dash1 or not dash2:
            return None
        
        prompt = f"""
            You are an expert at comparing KPI dashboards.
            
            Dashboard 1 Context:
            - Objective: {dash1['objective']}
            - Initial Analysis: {dash1['analysis']}
            
            Dashboard 2 Context:
            - Objective: {dash2['objective']}
            - Initial Analysis: {dash2['analysis']}
            
            Task: Provide a detailed comparison of the two dashboards. Highlight key differences, similarities, performance shifts, and potential strategic insights. Format the response clearly with headings.
        """
        return prompt

    def get_session_data(self) -> Optional[Dict]:
        """Get the data for the current active session."""
        if self.has_active_session():
            return st.session_state[st.session_state.current_session]
        return None
        
    def has_active_session(self) -> bool:
        """Check if there is an active session."""
        return st.session_state.current_session is not None and st.session_state[st.session_state.current_session] is not None
        
    def add_chat_message(self, role: str, message: str):
        """Add a new message to the chat history."""
        st.session_state.chat_history.append({"role": role, "message": message})
        
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
        
        session = st.session_state[st.session_state.current_session]
        
        # Format recent chat history (last 5 exchanges to keep context manageable)
        recent_chat = st.session_state.chat_history[-10:] if len(st.session_state.chat_history) > 10 else st.session_state.chat_history
        chat_context = ""
        if recent_chat:
            chat_context = "Recent conversation:\\n"
            for msg in recent_chat:
                chat_context += f"{msg['role'].title()}: {msg['message']}\\n"
        
        prompt = f"""You are analyzing a KPI dashboard. Here's the context:

            DASHBOARD OBJECTIVE: {session['objective']}
            
            INITIAL ANALYSIS:
            {session['analysis']}
            
            {chat_context}
            
            USER QUESTION: {user_message}
            
            Provide a helpful response focused on the dashboard analysis. Keep it concise and actionable."""
        return prompt
