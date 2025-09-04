import streamlit as st
import os
from PIL import Image
from dotenv import load_dotenv
from llm_service import gemini_inference, ollama_inference, gemini_chat_inference, ollama_chat_inference
from pdf_generator import create_pdf_report
from styles import custom_styles
from context_manager import DashboardContextManager

load_dotenv()

context_manager = DashboardContextManager()

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
    
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'comparison_analysis' not in st.session_state:
        st.session_state.comparison_analysis = None
        
    tab1, tab2 = st.tabs(["📈 Single Dashboard Analysis", "⚖️ Dashboard Comparison Tool"])
    
    with tab1:
        st.header("Analyze a Single Dashboard")
        model_choice = st.radio("Choose the model for analysis", ("Gemini (Online)", "Ollama (Local)"), horizontal=True, key="single_model_choice")

        uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
        objective = st.text_area("Provide a business objective for the analysis", height=100)
        
        
        if st.button("Generate Summary"):
            if uploaded_file and objective:
                with st.spinner('Analyzing the dashboard...'):
                    image = Image.open(uploaded_file)
                    
                    if model_choice == "Gemini (Online)":
                        analysis_result = gemini_inference(objective, [image])
                        model_used = "gemini"
                    else:
                        analysis_result = ollama_inference(os.getenv("OLLAMA_MODEL_NAME"), objective, [image])
                        model_used = "ollama"
                    
                    if analysis_result:
                        context_manager.create_session('single_dashboard', image, uploaded_file.name, objective, analysis_result, model_used)
                        st.session_state.comparison_analysis = None
                        st.session_state.analysis_result = analysis_result
                        st.rerun()
                    else:
                        st.error("Failed to get analysis from the model.")
            else:
                st.error("Please upload an image and provide a business objective.")

    with tab2:
        st.header("Compare Two Dashboards")
        
        comparison_model_choice = st.radio("Choose the model for comparison", ("Gemini (Online)", "Ollama (Local)"), horizontal=True, key="comparison_model_choice")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("<h4><i class='bi bi-speedometer'></i> Dashboard 1</h4>", unsafe_allow_html=True)
            uploaded_file1 = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="dashboard1_uploader")
            objective1 = st.text_area("Dashboard 1 Objective", height=100, key="objective1")
            
        with col2:
            st.markdown("<h4><i class='bi bi-speedometer2'></i> Dashboard 2</h4>", unsafe_allow_html=True)
            uploaded_file2 = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="dashboard2_uploader")
            objective2 = st.text_area("Dashboard 2 Objective", height=100, key="objective2")

        if uploaded_file1 and objective1 and uploaded_file2 and objective2:
            if st.button("Compare Dashboards"):
                with st.spinner("Analyzing and Comparing Dashboards..."):
                    image1 = Image.open(uploaded_file1)
                    image2 = Image.open(uploaded_file2)
                    
                    if comparison_model_choice == "Gemini (Online)":
                        analysis1 = gemini_inference(objective1, [image1]) 
                        analysis2 = gemini_inference(objective2, [image2])
                        model_used = "gemini"
                    else:
                        analysis1 = ollama_inference(os.getenv("OLLAMA_MODEL_NAME"), objective1, [image1])
                        analysis2 = ollama_inference(os.getenv("OLLAMA_MODEL_NAME"), objective2, [image2])
                        model_used = "ollama"
                    
                    context_manager.create_session('dashboard_one', image1, uploaded_file1.name, objective1, analysis1, model_used)
                    context_manager.create_session('dashboard_two', image2, uploaded_file2.name, objective2, analysis2, model_used)

                    comparison_prompt = context_manager.get_comparison_context()

                    if comparison_model_choice == "Gemini (Online)":
                        comparison_result = gemini_chat_inference(comparison_prompt)
                    else:
                        comparison_result = ollama_chat_inference(os.getenv("OLLAMA_MODEL_NAME"), comparison_prompt)
                    
                    st.session_state.comparison_analysis = comparison_result
                    st.rerun()

    st.markdown("---")
    
    if st.session_state.get('comparison_analysis'):
        st.subheader("Dashboard Comparison Analysis")
        st.write(st.session_state.comparison_analysis)
        
        pdf_bytes = generate_pdf_report(
            "Dashboard Comparison Analysis", 
            st.session_state.comparison_analysis, 
            "dashboard_comparison_report.pdf"
        )
        st.download_button(
            label="Download Comparison PDF Report",
            data=pdf_bytes,
            file_name="dashboard_comparison_report.pdf",
            mime="application/pdf"
        )
        
    elif context_manager.has_active_session():
        st.subheader("Dashboard Analysis")
        session_data = context_manager.get_session_data()
        
        if session_data:
            st.image(session_data["image_pil"], caption=session_data["filename"], width=400)
            
            if session_data['analysis']:
                st.markdown("### Analysis:")
                st.write(session_data['analysis'])

                pdf_bytes = generate_pdf_report(session_data['objective'], session_data['analysis'], session_data['filename'])
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"{session_data['filename'].split('.')[0]}_report.pdf",
                    mime="application/pdf"
                )

            st.info("Start a conversation about your dashboard!")

    if context_manager.has_active_session() or st.session_state.get('comparison_analysis'):
        for message in context_manager.get_chat_history():
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

        user_input = st.chat_input("Ask about your dashboard...")
        
        if user_input:
            handle_chat_message(user_input)

def handle_chat_message(user_message: str):
    if not context_manager.has_active_session() and not st.session_state.get('comparison_analysis'):
        st.error("No active session found. Please upload a dashboard first.")
        return
    
    try:
        context_manager.add_chat_message("user", user_message)
        
        with st.spinner("Getting response..."):
            if st.session_state.get('comparison_analysis'):
                chat_prompt = f"""
                    You are an expert at analyzing dashboard comparisons. Here's the context:
                    
                    COMPARISON ANALYSIS:
                    {st.session_state.comparison_analysis}
                    
                    USER QUESTION: {user_message}
                    
                    Provide a helpful response focused on the comparison.
                """
                ai_response = gemini_chat_inference(chat_prompt)
            else:
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
                st.error("Failed to get a response from the model.")
    except Exception as e:
        st.error(f"An error occurred during chat inference: {e}")

if __name__ == "__main__":
    main()