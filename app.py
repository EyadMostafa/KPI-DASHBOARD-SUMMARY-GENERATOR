import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
from llm_service import gemini_inference, ollama_inference, gemini_chat_inference, ollama_chat_inference
from pdf_generator import create_pdf_report
from utils import image_to_base64
from styles import custom_styles
from context_manager import context_manager

load_dotenv()

@st.cache_data
def generate_pdf_report(objective, analysis, filename):
    return create_pdf_report(objective, analysis, filename) 

def main():
    st.set_page_config(
        page_title="KPI Dashboard Analyzer",
        layout="wide"
    )

    st.markdown(custom_styles(), unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>📊 KPI Dashboard Analyzer</h1>
        <h3>AI-Powered Dashboard Analysis and Insights</h3>
        <p>Upload your KPI dashboard image and provide the business objective to get detailed analysis and strategic recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize legacy state for backward compatibility
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
        st.session_state.footer_text = "Choose a model to start"
        
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Dashboard")
        uploaded_file = st.file_uploader(
            "Choose a KPI dashboard image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload your KPI dashboard image (PNG, JPG, or JPEG format)"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Dashboard", use_container_width=True)
            st.info(f"**File:** {uploaded_file.name}\n**Size:** {image.size}\n**Mode:** {image.mode}")
            
    with col2:
        st.header("🎯 Dashboard Objective")
        dashboard_objective = st.text_area(
            "Enter the business objective for this dashboard",
            placeholder="e.g., To monitor employee distribution and performance metrics to support strategic workforce planning.",
            height=150
        )
        
        model_choice = st.selectbox(
            "Choose a Model Source",
            ("API Model (Gemini)", "Local Model (Ollama)")
        )
        
        with st.expander("💡 Example Objectives"):
            st.markdown("""
            - **HR:** To monitor employee distribution to support workforce planning.
            - **Sales:** To track revenue, customer acquisition, and sales team productivity.
            - **Finance:** To monitor key financial metrics and ensure fiscal health.
            """)
    
    st.header("🔍 Analysis")
    
    if uploaded_file is not None and len(dashboard_objective.strip()) > 0:
        if st.button("🚀 Analyze Dashboard", type="primary", use_container_width=True):
            with st.spinner("Analyzing dashboard... This may take a few moments."):
                uploaded_image_pil = Image.open(uploaded_file)
                
                if model_choice == "API Model (Gemini)":
                    analysis_result = gemini_inference(dashboard_objective, [uploaded_image_pil])
                    model_type = "gemini"
                    st.session_state.footer_text = "Powered by Gemini Pro Vision Model"
                else: # Local Model (Ollama)
                    ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen2.5vl:7b")
                    analysis_result = ollama_inference(ollama_model_name, dashboard_objective, [uploaded_image_pil])
                    model_type = "ollama"
                    st.session_state.footer_text = f"Powered by Local Model ({ollama_model_name})"
                
                if analysis_result:
                    # Create session using context manager
                    session_created = context_manager.create_session(
                        image=uploaded_image_pil,
                        filename=uploaded_file.name,
                        objective=dashboard_objective,
                        analysis=analysis_result,
                        model_used=model_type
                    )
                    
                    if session_created:
                        st.success("✅ Analysis Complete! You can now chat about this dashboard.")
                        st.rerun()
                    else:
                        st.error("Failed to create analysis session.")
                else:
                    st.error("Failed to process the request. Please check your API key or local model setup.")
    
    if context_manager.has_active_session():
        session_data = context_manager.get_session_data()
        
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Analysis Results", "🎯 Objective", "🖼️ Dashboard", "💬 Chat"])
        
        with tab1:
            st.markdown("### AI Analysis Results")
            st.markdown(session_data["analysis"])
        
        if st.download_button(
            label="📥 Download PDF Report",
            data=generate_pdf_report(session_data["objective"], session_data["analysis"], session_data["filename"]),
            file_name=f"dashboard_analysis_{session_data['filename'].split('.')[0]}.pdf",
            mime="application/pdf",
            key="download_pdf"
        ):
            st.success("PDF downloaded!")
        
        with tab2:
            st.markdown("### Dashboard Objective")
            st.info(session_data["objective"])
        
        with tab3:
            st.markdown("### Dashboard Image")
            st.image(session_data["image_pil"], caption="Analyzed Dashboard", use_container_width=True)
        
        with tab4:
            render_chat_interface()
    
    elif uploaded_file is None:
        st.info("👆 Please upload a dashboard image to get started.")
    elif not dashboard_objective.strip():
        st.info("📝 Please enter the dashboard objective to proceed with analysis.")
    
    st.markdown(f"""
    <div class="footer-text">
        <strong>{st.session_state.footer_text}</strong> | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

def render_chat_interface():
    """Render the chat interface."""
    st.markdown("### 💬 Chat About Your Dashboard")
    
    # Show chat history
    chat_history = context_manager.get_chat_history()
    
    if chat_history:
        for msg in chat_history:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['message']}")
            else:
                st.markdown(f"**AI:** {msg['message']}")
            st.markdown("---")
    else:
        st.info("Start a conversation about your dashboard!")
    
    # Chat input
    user_input = st.chat_input("Ask about your dashboard...")
    
    if user_input:
        handle_chat_message(user_input)

def handle_chat_message(user_message: str):
    """Handle user chat message and get AI response."""
    if not context_manager.has_active_session():
        st.error("No active session found.")
        return
    
    try:
        # Add user message
        context_manager.add_chat_message("user", user_message)
        
        # Prepare context and get AI response
        with st.spinner("Getting response..."):
            chat_prompt = context_manager.prepare_chat_context(user_message)
            session_data = context_manager.get_session_data()
            model_type = session_data["model_used"]
            
            if model_type == "gemini":
                ai_response = gemini_chat_inference(chat_prompt)
            else:
                ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen2.5vl:7b")
                ai_response = ollama_chat_inference(ollama_model_name, chat_prompt)
            
            if ai_response:
                context_manager.add_chat_message("assistant", ai_response)
                st.rerun()
            else:
                st.error("Failed to get AI response.")
                
    except Exception as e:
        st.error(f"Chat error: {e}")

if __name__ == "__main__":
    main()