import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv

# Import functions from your new modules
from llm_service import gemini_inference, ollama_inference
from pdf_generator import create_pdf_report
from utils import image_to_base64
from styles import custom_styles

# Load environment variables
load_dotenv()

def main():
    # Apply custom CSS
    st.markdown(custom_styles(), unsafe_allow_html=True)
    
    # Custom Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 KPI Dashboard Analyzer</h1>
        <h3>AI-Powered Dashboard Analysis and Insights</h3>
        <p>Upload your KPI dashboard image and provide the business objective to get detailed analysis and strategic recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for analysis results
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
                    st.session_state.footer_text = "Powered by Gemini Pro Vision Model"
                else: # Local Model (Ollama)
                    ollama_model_name = os.getenv("OLLAMA_MODEL_NAME", "qwen-2.5-4b-instruct-vision")
                    analysis_result = ollama_inference(ollama_model_name, dashboard_objective, [uploaded_image_pil])
                    st.session_state.footer_text = f"Powered by Local Model ({ollama_model_name})"
                
                if analysis_result:
                    st.session_state.analysis_result = analysis_result
                    st.session_state.analysis_objective = dashboard_objective
                    st.session_state.analysis_image = uploaded_image_pil
                    st.session_state.analysis_filename = uploaded_file.name
                    st.success("✅ Analysis Complete!")
                    st.rerun()
                else:
                    st.error("Failed to process the request. Please check your API key or local model setup.")
    
    if st.session_state.analysis_result is not None:
        tab1, tab2, tab3 = st.tabs(["📋 Analysis Results", "🎯 Objective", "🖼️ Dashboard"])
        
        with tab1:
            st.markdown("### AI Analysis Results")
            st.markdown(st.session_state.analysis_result)
            
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
    
    st.markdown(f"""
    <div class="footer-text">
        <strong>{st.session_state.footer_text}</strong> | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()