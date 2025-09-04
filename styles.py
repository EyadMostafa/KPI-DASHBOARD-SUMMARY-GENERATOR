def custom_styles():
    return """
    <style>
    /* Import Google Fonts matching I-Score's modern aesthetic */
    @import url('https://fonts.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
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
        color: white !important; /* Set text color to visible */
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: vertical !important;
        padding: 1rem !important;
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
    
    /* NEW: Radio button styling to fix color visibility */
    .stRadio label {
        color: var(--iscore-dark-charcoal) !important; /* Make radio label visible */
    }
    
    .stRadio [data-testid="stFormSubmitButton"] {
        color: white !important;
    }
    
    .stRadio p {
        color: var(--iscore-dark-charcoal) !important; /* Make radio option text visible */
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
    
    /* FIXED Alert components styled with I-Score branding */
    
    /* Info alerts (st.info) */
    .stAlert[data-baseweb="notification"]:has([data-testid="stNotificationContentInfo"]) {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-15), var(--iscore-teal-alpha-05)) !important;
        border-left: 6px solid var(--iscore-teal-primary) !important;
        color: var(--iscore-dark-charcoal) !important;
    }
    
    /* Success alerts (st.success) */
    .stAlert[data-baseweb="notification"]:has([data-testid="stNotificationContentSuccess"]) {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-20), var(--iscore-teal-alpha-10)) !important;
        border-left: 6px solid var(--iscore-teal-primary) !important;
        color: var(--iscore-dark-charcoal) !important;
    }
    
    /* Error alerts (st.error) */
    .stAlert[data-baseweb="notification"]:has([data-testid="stNotificationContentError"]) {
        background: linear-gradient(145deg, var(--iscore-purple-alpha-15), var(--iscore-purple-alpha-05)) !important;
        border-left: 6px solid var(--iscore-purple-primary) !important;
        color: var(--iscore-dark-charcoal) !important;
    }
    
    /* Warning alerts (st.warning) */
    .stAlert[data-baseweb="notification"]:has([data-testid="stNotificationContentWarning"]) {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-15), var(--iscore-teal-alpha-05)) !important;
        border-left: 6px solid var(--iscore-teal-dark) !important;
        color: var(--iscore-dark-charcoal) !important;
    }
    
    /* Ensure all alert text is visible with proper color - Multiple fallback approaches */
    .stAlert * {
        color: var(--iscore-dark-charcoal) !important;
    }
    
    .stAlert div,
    .stAlert p,
    .stAlert span {
        color: var(--iscore-dark-charcoal) !important;
    }
    
    /* Legacy alert class support for older Streamlit versions */
    .stInfo,
    .stSuccess, 
    .stError,
    .stWarning {
        background: linear-gradient(145deg, var(--iscore-teal-alpha-15), var(--iscore-teal-alpha-05)) !important;
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
    }
    
    .stError {
        background: linear-gradient(145deg, var(--iscore-purple-alpha-15), var(--iscore-purple-alpha-05)) !important;
        border-color: var(--iscore-purple-primary) !important;
        border-left-color: var(--iscore-purple-primary) !important;
        box-shadow: 0 4px 15px var(--iscore-purple-alpha-20) !important;
    }
    
    .stWarning {
        border-color: var(--iscore-teal-dark) !important;
        border-left-color: var(--iscore-teal-dark) !important;
    }
    
    /* Additional fallback selectors for alert text visibility */
    [data-baseweb="notification"] {
        color: var(--iscore-dark-charcoal) !important;
    }
    
    [data-baseweb="notification"] * {
        color: var(--iscore-dark-charcoal) !important;
    }
    
    div[data-testid*="stNotification"] {
        color: var(--iscore-dark-charcoal) !important;
    }
    
    div[data-testid*="stNotification"] * {
        color: var(--iscore-dark-charcoal) !important;
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
    
    /* Spinner customization */
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
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border: 2px solid var(--iscore-teal-primary) !important;
        border-radius: 10px !important;
        color: var(--iscore-dark-charcoal) !important;
        background: linear-gradient(145deg, var(--iscore-teal-alpha-05), var(--iscore-purple-alpha-05)) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--iscore-purple-primary) !important;
        box-shadow: 0 0 0 2px var(--iscore-purple-alpha-20) !important;
    }
    
    /* Markdown content styling */
    .stMarkdown {
        color: var(--iscore-dark-charcoal) !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.6 !important;
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
    
    /* Chat messages and input styling */
    .stChatInputContainer {
        border-top: 2px solid var(--iscore-gray-200);
        padding-top: 1rem;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .stChatMessage:nth-child(even) {
        background: var(--iscore-teal-alpha-05);
        border-left: 4px solid var(--iscore-teal-primary);
    }
    .stChatMessage:nth-child(odd) {
        background: var(--iscore-purple-alpha-05);
        border-right: 4px solid var(--iscore-purple-primary);
        margin-left: auto;
    }
    </style>
    """ 