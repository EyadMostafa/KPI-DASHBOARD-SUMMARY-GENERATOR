"""
Dashboard Similarity Detection Module

This module contains functions to detect if two dashboard images are similar
or identical before performing comparison analysis.
"""

import streamlit as st
import os
from llm_service import gemini_inference, ollama_inference


def detect_dashboard_similarity(image1, image2, model_choice):
    """
    Detect if two dashboard images are similar or identical.
    
    Args:
        image1: First PIL Image object
        image2: Second PIL Image object  
        model_choice: String indicating which model to use
    
    Returns:
        dict: {
            'are_similar': bool,
            'similarity_level': str,  # 'identical', 'very_similar', 'somewhat_similar', 'different'
            'similarity_percentage': int,  # 0-100
            'message': str
        }
    """
    try:
        similarity_prompt = """
Please analyze these two dashboard images and determine their similarity level.

Compare the following aspects:
- Overall layout and structure
- Data visualizations (charts, graphs, tables)
- Numbers, metrics, and KPIs shown
- Color schemes and styling
- Content and data points
- Dashboard components and sections

Respond with ONLY a JSON object in this exact format:
{
    "similarity_level": "identical|very_similar|somewhat_similar|different",
    "similarity_percentage": 85,
    "reasoning": "Brief explanation of why they are similar/different"
}

Guidelines:
- "identical": Same dashboard, same data, same layout (95-100%)
- "very_similar": Same dashboard with minor differences (80-94%)
- "somewhat_similar": Similar dashboard type but different data (50-79%)
- "different": Completely different dashboards (0-49%)

Be accurate and strict in your assessment.
"""
        
        if model_choice == "Gemini (Online)":
            result = gemini_inference(similarity_prompt, [image1, image2])
        else:
            result = ollama_inference(os.getenv("OLLAMA_MODEL_NAME"), similarity_prompt, [image1, image2])
        
        if result:
            return parse_similarity_result(result)
        else:
            return create_default_similarity_result("Error analyzing similarity")
            
    except Exception as e:
        st.error(f"Error detecting dashboard similarity: {e}")
        return create_default_similarity_result("Error occurred during similarity analysis")


def parse_similarity_result(result):
    """
    Parse the AI response to extract similarity information.
    
    Args:
        result: String response from AI model
    
    Returns:
        dict: Parsed similarity information
    """
    try:
        import json
        import re
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            
            similarity_level = data.get('similarity_level', 'different').lower()
            similarity_percentage = int(data.get('similarity_percentage', 0))
            reasoning = data.get('reasoning', 'No reasoning provided')
            
            # Determine if they are similar enough to be considered the same
            are_similar = similarity_percentage >= 80
            
            return {
                'are_similar': are_similar,
                'similarity_level': similarity_level,
                'similarity_percentage': similarity_percentage,
                'reasoning': reasoning,
                'message': create_similarity_message(similarity_level, similarity_percentage, reasoning)
            }
        else:
            # Fallback: try to extract information from text
            return parse_text_similarity_result(result)
            
    except Exception as e:
        return create_default_similarity_result(f"Error parsing similarity result: {e}")


def parse_text_similarity_result(result):
    """
    Fallback method to parse similarity from text response.
    
    Args:
        result: String response from AI model
    
    Returns:
        dict: Parsed similarity information
    """
    result_lower = result.lower()
    
    # Extract percentage if mentioned
    import re
    percentage_match = re.search(r'(\d+)%', result)
    similarity_percentage = int(percentage_match.group(1)) if percentage_match else 50
    
    # Determine similarity level based on keywords
    if 'identical' in result_lower or 'same' in result_lower:
        similarity_level = 'identical'
    elif 'very similar' in result_lower or 'almost identical' in result_lower:
        similarity_level = 'very_similar'
    elif 'somewhat similar' in result_lower or 'similar' in result_lower:
        similarity_level = 'somewhat_similar'
    else:
        similarity_level = 'different'
    
    are_similar = similarity_percentage >= 80
    
    return {
        'are_similar': are_similar,
        'similarity_level': similarity_level,
        'similarity_percentage': similarity_percentage,
        'reasoning': result,
        'message': create_similarity_message(similarity_level, similarity_percentage, result)
    }


def create_similarity_message(similarity_level, similarity_percentage, reasoning):
    """
    Create a user-friendly message based on similarity analysis.
    
    Args:
        similarity_level: String indicating similarity level
        similarity_percentage: Integer percentage (0-100)
        reasoning: String with AI reasoning
    
    Returns:
        str: Formatted message for the user
    """
    if similarity_level == 'identical':
        return f"""
        🔄 **Identical Dashboards Detected** ({similarity_percentage}% similar)
        
        You have uploaded the same dashboard twice. Since these are identical, there's no meaningful comparison to make.
        
        **Recommendation:** Upload two different dashboards to get a meaningful comparison analysis.
        
        **AI Reasoning:** {reasoning}
        """
    elif similarity_level == 'very_similar':
        return f"""
        ⚠️ **Very Similar Dashboards** ({similarity_percentage}% similar)
        
        These dashboards are very similar with only minor differences. The comparison may not provide much insight.
        
        **Recommendation:** Consider uploading more distinct dashboards for better comparison analysis.
        
        **AI Reasoning:** {reasoning}
        """
    elif similarity_level == 'somewhat_similar':
        return f"""
        📊 **Somewhat Similar Dashboards** ({similarity_percentage}% similar)
        
        These dashboards have some similarities but also notable differences. A comparison analysis will be performed.
        
        **AI Reasoning:** {reasoning}
        """
    else:
        return f"""
        ✅ **Different Dashboards** ({similarity_percentage}% similar)
        
        These are distinct dashboards suitable for comparison analysis.
        
        **AI Reasoning:** {reasoning}
        """


def create_default_similarity_result(error_message):
    """
    Create a default similarity result when analysis fails.
    
    Args:
        error_message: String describing the error
    
    Returns:
        dict: Default similarity result
    """
    return {
        'are_similar': False,
        'similarity_level': 'unknown',
        'similarity_percentage': 0,
        'reasoning': error_message,
        'message': f"❌ **Similarity Analysis Failed**\n\n{error_message}\n\nProceeding with comparison analysis..."
    }


def should_proceed_with_comparison(similarity_result):
    """
    Determine if comparison should proceed based on similarity analysis.
    
    Args:
        similarity_result: Dict from detect_dashboard_similarity()
    
    Returns:
        bool: True if comparison should proceed, False otherwise
    """
    similarity_level = similarity_result.get('similarity_level', 'different')
    similarity_percentage = similarity_result.get('similarity_percentage', 0)
    
    # Don't proceed if they are identical or very similar
    if similarity_level in ['identical'] or similarity_percentage >= 95:
        return False
    
    # Proceed for different or somewhat similar dashboards
    return True
