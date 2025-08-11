import streamlit as st
import os
import tempfile
import sys

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from ui.terminal.chatbot import KFGChatbot
from config.config import Config
import logging
import json

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="KFG Policy Chatbot",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple Clean Chatbot Interface
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables for Brand Colors */
    :root {
        --primary-red: #C32029;
        --primary-yellow: #D1C529;
        --white: #ffffff;
        --light-gray: #f8fafc;
        --dark-gray: #1e293b;
        --blue: #3b82f6;
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--light-gray);
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Simple Header */
    .header {
        background: var(--primary-red);
        padding: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .header-content {
        max-width: 500px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .header-logo {
        width: 32px;
        height: 32px;
        object-fit: contain;
    }
    
    .header-title {
        color: var(--white);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Main Content Area - Clean and Simple */
    .main-content {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        background: var(--white);
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border: 1px solid #e5e7eb;
    }
    
    /* Chat Messages - Direct on White Background */
    .message {
        margin: 0.75rem 0;
        padding: 0.8rem 1rem;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .user-message {
        background: var(--blue);
        color: var(--white);
        margin-left: auto;
        margin-right: 0;
        border-radius: 18px 18px 4px 18px;
    }
    
    .bot-message {
        background: #f8fafc;
        color: var(--dark-gray);
        margin-right: auto;
        margin-left: 0;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #e5e7eb;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-red);
        box-shadow: 0 0 0 3px rgba(195, 32, 41, 0.1);
        outline: none;
    }
    
    /* Send Button */
    .stButton > button {
        background: var(--primary-red);
        color: var(--white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
        min-width: 80px;
    }
    
    .stButton > button:hover {
        background: #a01a22;
        transform: translateY(-1px);
    }
    
    /* Simple Footer - Clean */
    .footer {
        text-align: center;
        padding: 1rem 0;
        margin-top: 2rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .footer-logo {
        width: 35px;
        height: 35px;
        object-fit: contain;
        margin-bottom: 0.5rem;
    }
    
    .footer-text {
        color: var(--dark-gray);
        font-size: 0.75rem;
        opacity: 0.6;
        margin: 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-content {
            max-width: 90%;
            margin: 2rem auto;
            padding: 1.25rem;
        }
        
        .header-content {
            max-width: 90%;
        }
        
        .message {
            max-width: 85%;
        }
        
        .header-title {
            font-size: 1.1rem;
        }
        
        .chat-container {
            max-height: 300px;
        }
    }
    
    @media (max-width: 480px) {
        .main-content {
            max-width: 95%;
            margin: 1.5rem auto;
            padding: 1rem;
        }
        
        .header-title {
            font-size: 1rem;
        }
        
        .message {
            max-width: 90%;
            font-size: 0.85rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def get_image_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as image_file:
            import base64
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image {image_path}: {e}")
        return ""

@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot with caching"""
    try:
        chatbot = KFGChatbot()
        return chatbot
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return None

def main():
    # Simple Header with Brand Logo
    st.markdown("""
    <div class="header">
        <div class="header-content">
            <img src="data:image/png;base64,{}" alt="KFG Brand Logo" class="header-logo">
            <h1 class="header-title">Kazi Farms Policy Chatbot</h1>
        </div>
    </div>
    """.format(get_image_base64("ui/logos/brand_01.png")), unsafe_allow_html=True)
    
    # Main Content Container
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    if not chatbot:
        st.error("❌ Chatbot initialization failed. Please check your configuration.")
        return
    
    # Simple Chat Interface - No Extra Panels
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display existing chat messages
    for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history):
        # User message (right side, blue)
        st.markdown(f'<div class="message user-message">{user_msg}</div>', unsafe_allow_html=True)
        
        # Bot message (left side, white)
        st.markdown(f'<div class="message bot-message">{bot_msg}</div>', unsafe_allow_html=True)
    
    # Simple Input Section - Clean and Minimal
    query = st.text_input(
        "Ask a question about our policies...", 
        placeholder="Ask a question about our policies...",
        key="chat_input"
    )
    
    # Send Button - Centered
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Send", use_container_width=True):
            if query.strip():
                with st.spinner("Searching..."):
                    # Get chatbot response
                    chat_response = chatbot.chat(query)
                    
                    if chat_response.get("error"):
                        st.error(f"Error: {chat_response['error']}")
                    else:
                        # Add to chat history
                        st.session_state.chat_history.append((query, chat_response['response']))
                        st.rerun()
    
    # Clear chat button - Only when there are messages
    if st.session_state.chat_history:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Clear Chat History", use_container_width=True, key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Footer with Sysnova Logo - Simple
    st.markdown("""
    <div class="footer">
        <img src="data:image/png;base64,{}" alt="Sysnova Logo" class="footer-logo">
        <p class="footer-text">sysnova</p>
    </div>
    """.format(get_image_base64("ui/logos/sysnova--logo--3.png")), unsafe_allow_html=True)
    
    # Close main content container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 