# 📊 KPI Dashboard Analyzer

An AI-powered web application that analyzes KPI dashboards and provides strategic insights using computer vision and natural language processing.

## 🌟 Features

- **AI-Powered Analysis**: Leverages Ollama's Qwen 2.5 Vision model for intelligent dashboard interpretation
- **Image Upload**: Supports PNG, JPG, and JPEG dashboard images
- **Business Context**: Analyzes dashboards based on specific business objectives
- **Professional Reports**: Generates branded PDF reports with I-Score styling
- **Modern UI**: Clean, responsive interface with custom branding
- **Real-time Processing**: Instant analysis with progress feedback

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** installed on your system
3. **Qwen 2.5 Vision model** pulled in Ollama

### Installation

1. **Install dependencies**:
   ```bash
   pip install streamlit ollama pillow reportlab
   ```

2. **Set up Ollama and pull the required model**:
   ```bash
   # Install Ollama (if not already installed)
   # Visit https://ollama.com for installation instructions
   
   # Pull the vision model
   ollama pull qwen2.5vl:7b
   ```

3. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📋 How to Use

### Step 1: Upload Dashboard
- Click "Choose a KPI dashboard image" 
- Select a PNG, JPG, or JPEG file of your dashboard
- Preview will appear automatically

### Step 2: Define Objective
- Enter your business objective in the text area
- Be specific about what the dashboard should achieve
- Use the example objectives for guidance

### Step 3: Analyze
- Click "🚀 Analyze Dashboard"
- Wait for AI processing to complete
- Review results in the analysis tabs

### Step 4: Download Report
- View detailed analysis in the "Analysis Results" tab
- Click "📥 Download PDF Report" for a professional report
- Share insights with stakeholders

## 🎯 Example Use Cases

### HR Dashboard Analysis
```
Objective: Monitor employee distribution and performance metrics 
to support workforce planning and talent management.
```

### Sales Dashboard Analysis
```
Objective: Track revenue performance, customer acquisition, 
and sales team productivity to drive business growth.
```

### Financial Dashboard Analysis
```
Objective: Monitor key financial metrics including revenue, 
expenses, and profitability to ensure fiscal health.
```

## 📁 Project Structure

```
llm/
├── streamlit_app.py          # Main application file
├── README.md                 # This file
```

## 🔧 Technical Details

### Core Dependencies
- **Streamlit**: Web application framework
- **Ollama**: Local AI model inference
- **PIL (Pillow)**: Image processing
- **ReportLab**: PDF generation
- **Base64**: Image encoding

### AI Model
- **Model**: Qwen 2.5 Vision (7B parameters)
- **Capabilities**: Multimodal analysis (text + images)
- **Local Processing**: Runs entirely on your machine

### Features Breakdown

#### Image Processing
- Converts images to base64 for AI processing
- Supports RGB conversion for compatibility
- Error handling for corrupted files

#### AI Analysis
- Structured prompts for consistent results
- Business context integration
- Strategic recommendations generation

#### PDF Reports
- Professional I-Score branding
- Custom styling and layout
- Downloadable format for sharing

## 🎨 UI Customization

The application features a custom-designed interface with:
- **I-Score Brand Colors**: Teal (#45BCC3) and Purple (#4F3C8F)
- **Modern Typography**: Inter and Space Grotesk fonts
- **Responsive Design**: Works on desktop and mobile
- **Professional Styling**: Gradients, shadows, and animations

## ⚠️ Troubleshooting

### Model Not Found Error
```bash
# Pull the required model
ollama pull qwen2.5vl:7b

# Verify installation
ollama list
```

### Image Processing Errors
- Ensure image file is not corrupted
- Check file format (PNG, JPG, JPEG only)
- Verify file size is reasonable (<10MB recommended)

### Port Already in Use
```bash
# Run on different port
streamlit run streamlit_app.py --server.port 8502
```

## 🔒 Privacy & Security

- **Local Processing**: All analysis happens on your machine
- **No Data Upload**: Images and data never leave your system
- **Secure**: No external API calls or data transmission

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

---

**Built with ❤️ using Streamlit and Ollama**