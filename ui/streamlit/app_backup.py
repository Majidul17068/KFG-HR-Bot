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

# Professional Navigation-Based Design with Bangladesh Flag Colors
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
    
    /* CSS Variables for Brand Colors */
    :root {
        --bd-green: #006a4e;
        --bd-red: #f42a41;
        --bd-yellow: #ffd700;
        --kfg-green: #2d5a27;
        --kfg-gold: #d4af37;
        --sysnova-blue: #1e40af;
        --white: #ffffff;
        --light-gray: #f8fafc;
        --dark-gray: #1e293b;
    }
    
    /* Global Styles */
    .main {
        font-family: 'Poppins', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--light-gray);
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navigation Bar */
    .navbar {
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        padding: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        border-bottom: 3px solid var(--bd-yellow);
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .brand-logo {
        width: 50px;
        height: 50px;
        background: var(--bd-yellow);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--bd-green);
        border: 3px solid var(--bd-red);
    }
    
    .brand-text {
        color: var(--white);
        font-size: 1.5rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .nav-menu {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .nav-item {
        color: var(--white);
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .nav-item.active {
        background: var(--bd-yellow);
        color: var(--bd-green);
        font-weight: 600;
    }
    
    /* Main Content Area */
    .main-content {
        margin-top: 100px;
        padding: 2rem;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Page Header */
    .page-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        border-radius: 20px;
        color: var(--white);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        border: 2px solid var(--bd-yellow);
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 1rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .page-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        margin: 0;
        opacity: 0.9;
    }
    
    /* Enhanced Chat Messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        color: var(--white);
        border-left: 6px solid var(--bd-yellow);
        margin-left: 2rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, var(--bd-red) 0%, #dc2626 100%);
        color: var(--white);
        border-left: 6px solid var(--bd-yellow);
        margin-right: 2rem;
    }
    
    /* Modern Cards */
    .info-card {
        background: var(--white);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid var(--bd-green);
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-color: var(--bd-yellow);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        color: var(--white);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(45, 90, 39, 0.4);
        border: 2px solid var(--bd-yellow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(45, 90, 39, 0.6);
        background: linear-gradient(135deg, var(--kfg-green) 0%, var(--bd-green) 100%);
    }
    
    /* Secondary Button Style */
    .btn-secondary {
        background: linear-gradient(135deg, var(--bd-yellow) 0%, #fbbf24 100%) !important;
        color: var(--bd-green) !important;
        border: 2px solid var(--bd-green) !important;
    }
    
    /* Tabs Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--light-gray);
        border-radius: 12px;
        padding: 8px;
        border: 2px solid var(--bd-green);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: var(--white);
        border-radius: 8px;
        color: var(--bd-green);
        font-weight: 500;
        border: 1px solid var(--bd-green);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        color: var(--white);
        border-color: var(--bd-yellow);
    }
    
    /* Input Enhancement */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid var(--bd-green);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--bd-yellow);
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
    }
    
    /* Status Indicators */
    .status-success {
        color: var(--bd-green);
        font-weight: 600;
        background: rgba(45, 90, 39, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 2px solid var(--bd-green);
    }
    
    .status-error {
        color: var(--bd-red);
        font-weight: 600;
        background: rgba(244, 42, 65, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 2px solid var(--bd-red);
    }
    
    .status-info {
        color: var(--sysnova-blue);
        font-weight: 600;
        background: rgba(30, 64, 175, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 2px solid var(--sysnova-blue);
    }
    
    /* Filter Section */
    .filter-section {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 2px solid var(--bd-green);
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, var(--bd-green) 0%, var(--kfg-green) 100%);
        color: var(--white);
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
        border-top: 3px solid var(--bd-yellow);
        border-radius: 20px 20px 0 0;
    }
    
    .footer-logo {
        width: 60px;
        height: 60px;
        background: var(--sysnova-blue);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--white);
        margin-bottom: 1rem;
        border: 3px solid var(--bd-yellow);
    }
    
    .footer-text {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .nav-container {
            padding: 0 1rem;
            flex-direction: column;
            gap: 1rem;
        }
        
        .nav-menu {
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .page-title {
            font-size: 2rem;
        }
        
        .main-content {
            padding: 1rem;
        }
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border: 3px solid rgba(45, 90, 39, 0.3);
        border-top: 3px solid var(--bd-green);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

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
    # Navigation Bar
    st.markdown("""
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">
                <div class="brand-logo">🏢</div>
                <div class="brand-text">KFG Policy Chatbot</div>
            </div>
            <div class="nav-menu">
                <div class="nav-item active" onclick="document.querySelector('[data-testid=\\'stTabs\\']').scrollIntoView()">💬 Chat</div>
                <div class="nav-item" onclick="document.querySelector('[data-testid=\\'stTabs\\']').scrollIntoView()">📚 Search</div>
                <div class="nav-item" onclick="document.querySelector('[data-testid=\\'stTabs\\']').scrollIntoView()">📊 Analytics</div>
                <div class="nav-item" onclick="document.querySelector('[data-testid=\\'stTabs\\']').scrollIntoView()">📤 Upload</div>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)
    
    # Main Content Container
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Page Header
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🏢 Kazi Farms Group HR Policy Chatbot</h1>
        <p class="page-subtitle">Your intelligent AI assistant for KFG policy documents with confidence scoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = initialize_chatbot()
    if not chatbot:
        st.error("❌ Chatbot initialization failed. Please check your configuration.")
        return
    
    # Enhanced Sidebar with Modern Design
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600; color: white; margin: 0;">
                🔧 System Management
            </h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                Control panel for KFG Policy Chatbot
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # System Status Section
        st.markdown("### 📊 System Status")
        if st.button("🔍 Check System Status", use_container_width=True):
            with st.spinner("🔍 Checking system status..."):
                try:
                    stats = chatbot.vector_store.get_collection_stats()
                    if 'error' not in stats:
                        st.success(f"✅ Vector Database: {stats['total_documents']} documents")
                        
                        # Display stats in a nice format
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Documents", stats.get('total_documents', 0))
                        with col2:
                            st.metric("Total Chunks", stats.get('total_chunks', 0))
                        
                        # Show detailed stats in expander
                        with st.expander("📈 Detailed Statistics"):
                            st.json(stats)
                    else:
                        st.error(f"❌ Vector store error: {stats['error']}")
                except Exception as e:
                    st.error(f"❌ Error checking status: {e}")
        
        st.divider()
        
        # Document Management Section
        st.markdown("### 📁 Document Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📂 Organize", use_container_width=True):
                with st.spinner("📂 Organizing documents..."):
                    try:
                        results = chatbot.process_and_index_documents()
                        if results.get('indexed_documents'):
                            st.success(f"✅ {len(results['indexed_documents'])} docs organized")
                            
                            # Show organization summary
                            if results.get('organization_summary'):
                                summary = results['organization_summary']
                                with st.expander("📊 Organization Summary"):
                                    if 'categories' in summary:
                                        st.write("**Categories:**")
                                        for category, count in summary['categories'].items():
                                            st.write(f"  • {category}: {count}")
                                    
                                    if 'types' in summary:
                                        st.write("**Document Types:**")
                                        for doc_type, count in summary['types'].items():
                                            st.write(f"  • {doc_type}: {count}")
                        else:
                            st.error("❌ Organization failed")
                            if results.get('errors'):
                                for error in results['errors']:
                                    st.error(f"Error: {error}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        with col2:
            if st.button("🔍 Rebuild Index", use_container_width=True):
                with st.spinner("🔍 Rebuilding index..."):
                    try:
                        added_docs = chatbot.vector_store.rebuild_index()
                        if added_docs:
                            st.success(f"✅ Index rebuilt: {len(added_docs)} docs")
                        else:
                            st.error("❌ No documents added")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        st.divider()
        
        # Custom Prompts Management
        st.markdown("### 🎯 Custom Prompts")
        
        if st.button("📋 View Prompts", use_container_width=True):
            try:
                prompts = chatbot.get_custom_prompts()
                if prompts.get('success'):
                    st.success(f"✅ {prompts['total_prompts']} custom prompts found")
                    
                    for prompt_key, prompt_data in prompts['custom_prompts'].items():
                        with st.expander(f"📝 {prompt_key.replace('_', ' ').title()}"):
                            st.write("**Keywords:**")
                            for keyword in prompt_data['keywords']:
                                st.write(f"  • {keyword}")
                            st.write("**Response:**")
                            st.write(prompt_data['response'])
                            st.write(f"**Confidence:** {prompt_data['confidence_boost']}")
                else:
                    st.error(f"❌ Failed: {prompts.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        
        # Add new custom prompt
        with st.expander("➕ Add New Prompt"):
            new_prompt_key = st.text_input("Prompt Key", key="new_prompt_key", placeholder="e.g., salary_policy")
            new_keywords = st.text_area("Keywords (one per line)", key="new_keywords", placeholder="salary\nincrement\npolicy")
            new_response = st.text_area("Response", key="new_response", placeholder="Enter the response text...")
            new_confidence = st.slider("Confidence", 0.1, 1.0, 0.9, key="new_confidence")
            
            if st.button("Add Prompt", use_container_width=True):
                if new_prompt_key and new_keywords and new_response:
                    keywords_list = [k.strip() for k in new_keywords.split('\n') if k.strip()]
                    result = chatbot.add_custom_prompt(new_prompt_key, keywords_list, new_response, new_confidence)
                    
                    if result.get('success'):
                        st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.warning("⚠️ Please fill all fields")
        
        st.divider()
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📚 Index", use_container_width=True):
                try:
                    index_path = "./kfg_policy/document_index_v2.json"
                    if os.path.exists(index_path):
                        with open(index_path, 'r') as f:
                            index_data = json.load(f)
                        with st.expander("📚 Document Index"):
                            st.json(index_data)
                    else:
                        st.warning("⚠️ Index not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            if st.button("🗂️ Structure", use_container_width=True):
                try:
                    organized_path = "./kfg_policy/organized"
                    if os.path.exists(organized_path):
                        with st.expander("🗂️ Document Structure"):
                            # Show main organized files
                            organized_files = [f for f in os.listdir(organized_path) if f.endswith('_organized.txt')]
                            st.write(f"**Total:** {len(organized_files)}")
                            
                            # Show category structure
                            category_path = os.path.join(organized_path, "by_category")
                            if os.path.exists(category_path):
                                st.write("**By Category:**")
                                for category in os.listdir(category_path):
                                    if os.path.isdir(os.path.join(category_path, category)):
                                        category_files = [f for f in os.listdir(os.path.join(category_path, category)) if f.endswith('.txt')]
                                        st.write(f"  • {category}: {len(category_files)}")
                    else:
                        st.warning("⚠️ Organized folder not found")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        st.divider()
        
        # System Test
        st.markdown("### 🧪 System Test")
        if st.button("🔍 Test All Systems", use_container_width=True):
            with st.spinner("🧪 Testing systems..."):
                try:
                    test_results = chatbot.test_system()
                    
                    if test_results["overall"]:
                        st.success("✅ All systems operational")
                    else:
                        st.error("❌ System issues detected")
                        for component, status in test_results.items():
                            if component != "overall":
                                st.write(f"{component}: {'✅' if status else '❌'}")
                except Exception as e:
                    st.error(f"❌ Test failed: {e}")
        
        # Policy categories
        st.markdown("### 📂 Policy Categories")
        categories = chatbot.get_policy_categories()
        if categories:
            selected_category = st.selectbox("Filter by Category", ["All"] + categories)
        else:
            new_response = st.text_area("Response", key="new_response")
            new_confidence = st.slider("Confidence Boost", 0.1, 1.0, 0.9, key="new_confidence")
            
            if st.button("Add Custom Prompt"):
                if new_prompt_key and new_keywords and new_response:
                    keywords_list = [k.strip() for k in new_keywords.split('\n') if k.strip()]
                    result = chatbot.add_custom_prompt(new_prompt_key, keywords_list, new_response, new_confidence)
                    
                    if result.get('success'):
                        st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.warning("Please fill in all fields")
        
        st.divider()
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("📚 View Document Index"):
            try:
                index_path = "./kfg_policy/document_index_v2.json"
                if os.path.exists(index_path):
                    with open(index_path, 'r') as f:
                        index_data = json.load(f)
                    st.json(index_data)
                else:
                    st.warning("Document index not found. Run document organization first.")
            except Exception as e:
                st.error(f"Error reading index: {e}")
        
        if st.button("🗂️ View Organized Structure"):
            try:
                organized_path = "./kfg_policy/organized"
                if os.path.exists(organized_path):
                    st.write("**Organized Documents:**")
                    
                    # Show main organized files
                    organized_files = [f for f in os.listdir(organized_path) if f.endswith('_organized.txt')]
                    st.write(f"Total: {len(organized_files)}")
                    
                    # Show category structure
                    category_path = os.path.join(organized_path, "by_category")
                    if os.path.exists(category_path):
                        st.write("**By Category:**")
                        for category in os.listdir(category_path):
                            if os.path.isdir(os.path.join(category_path, category)):
                                category_files = [f for f in os.listdir(os.path.join(category_path, category)) if f.endswith('.txt')]
                                st.write(f"  • {category}: {len(category_files)}")
                    
                    # Show type structure
                    type_path = os.path.join(organized_path, "by_type")
                    if os.path.exists(type_path):
                        st.write("**By Type:**")
                        for doc_type in os.listdir(type_path):
                            if os.path.isdir(os.path.join(type_path, doc_type)):
                                type_files = [f for f in os.listdir(os.path.join(type_path, doc_type)) if f.endswith('.txt')]
                                st.write(f"  • {doc_type}: {len(type_files)}")
                else:
                    st.warning("Organized folder not found. Run document organization first.")
            except Exception as e:
                st.error(f"Error viewing structure: {e}")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # System status
        st.subheader("System Status")
        if st.button("🔍 Test System"):
            with st.spinner("Testing system components..."):
                test_results = chatbot.test_system()
                
                if test_results["overall"]:
                    st.success("✅ All systems operational")
                else:
                    st.error("❌ System issues detected")
                    for component, status in test_results.items():
                        if component != "overall":
                            st.write(f"{component}: {'✅' if status else '❌'}")
        
        # Document management
        st.subheader("📚 Document Management")
        if st.button("🔄 Reprocess Documents"):
            with st.spinner("Processing documents..."):
                results = chatbot.process_and_index_documents(force_reprocess=True)
                if results.get("errors"):
                    st.error(f"Errors: {results['errors']}")
                else:
                    st.success(f"✅ Processed {len(results.get('indexed_documents', []))} documents")
        

        
        # Policy categories
        st.subheader("📂 Policy Categories")
        categories = chatbot.get_policy_categories()
        if categories:
            selected_category = st.selectbox("Filter by Category", ["All"] + categories, key="sidebar_category_filter")
        else:
            selected_category = "All"
        
        # Document types
        doc_types = chatbot.get_document_types()
        if doc_types:
            selected_type = st.selectbox("Filter by Type", ["All"] + doc_types, key="sidebar_type_filter")
        else:
            selected_type = "All"
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📚 Policy Search", "📊 Analytics", "📤 Upload"])
    
    # Chat tab
    with tab1:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2rem; font-weight: 600; color: #1e293b; margin: 0;">
                💬 Ask About KFG Policies
            </h2>
            <p style="color: #64748b; font-size: 1rem; margin: 0.5rem 0 0 0;">
                Get instant answers with confidence scoring and source attribution
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat filters in a modern card
        with st.container():
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            st.markdown("### 🔍 Search Filters")
            col1, col2 = st.columns(2)
            with col1:
                category_filter = st.selectbox("Category Filter", ["None"] + categories, key="chat_category_filter") if categories else "None"
            with col2:
                type_filter = st.selectbox("Type Filter", ["None"] + doc_types, key="chat_type_filter") if doc_types else "None"
            
            if category_filter == "None":
                category_filter = None
            if type_filter == "None":
                type_filter = None
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced chat input
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        query = st.text_input(
            "Ask your question about KFG policies:", 
            placeholder="e.g., What is the TA-DA policy for officers?",
            help="Type your policy question here. The system will search through all available documents and provide a comprehensive answer."
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Ask Question", use_container_width=True):
                if query.strip():
                    with st.spinner("🔍 Searching for relevant policies..."):
                        # Apply filters
                        chat_response = chatbot.chat(
                            query, 
                            category_filter=category_filter if category_filter != "None" else None,
                            doc_type_filter=type_filter if type_filter != "None" else None
                        )
                        
                        if chat_response.get("error"):
                            st.error(f"❌ Error: {chat_response['error']}")
                        else:
                            # Display response in enhanced card
                            st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
                            st.markdown(chat_response['response'])
                            
                            # Enhanced source display
                            if chat_response.get('sources'):
                                st.markdown("---")
                                st.markdown("### 📚 Sources & Confidence Scores")
                                for i, source in enumerate(chat_response['sources'], 1):
                                    confidence_color = "#10b981" if source['similarity'] >= 0.7 else "#f59e0b" if source['similarity'] >= 0.5 else "#ef4444"
                                    st.markdown(f"""
                                    <div style="background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {confidence_color};">
                                        <strong>{i}. {source['filename']}</strong><br>
                                        <span style="color: {confidence_color}; font-weight: 600;">Confidence: {source['similarity']:.2f}</span><br>
                                        <small style="color: rgba(255,255,255,0.8);">Category: {source['category']} | Type: {source['document_type']}</small>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # Store in chat history
                            if 'chat_history' not in st.session_state:
                                st.session_state.chat_history = []
                            st.session_state.chat_history.append((query, chat_response['response']))
                            
                            # Success message
                            st.success("✅ Answer generated successfully!")
                else:
                    st.warning("⚠️ Please enter a question.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced chat history
        if 'chat_history' in st.session_state and st.session_state.chat_history:
            st.markdown("### 💭 Recent Conversations")
            for i, (user_msg, bot_msg) in enumerate(st.session_state.chat_history[-3:], 1):
                # User message
                st.markdown('<div class="chat-message user-message">', unsafe_allow_html=True)
                st.markdown(f"**You:** {user_msg}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Bot message
                st.markdown('<div class="chat-message bot-message">', unsafe_allow_html=True)
                st.markdown(f"**Bot:** {bot_msg[:200]}{'...' if len(bot_msg) > 200 else ''}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Clear history button
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Policy Search tab
    with tab2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-size: 2rem; font-weight: 600; color: #1e293b; margin: 0;">
                📚 Search KFG Policies
            </h2>
            <p style="color: #64748b; font-size: 1rem; margin: 0.5rem 0 0 0;">
                Advanced search with filters and relevance scoring
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search interface in modern card
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input(
                "Search policies:", 
                placeholder="e.g., salary increment, medical allowance, TA-DA policy",
                help="Enter keywords to search through all policy documents"
            )
        with col2:
            search_limit = st.slider("Results:", 1, 10, 5, help="Number of results to display")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Search Policies", use_container_width=True):
                if search_query.strip():
                    with st.spinner("🔍 Searching through policies..."):
                        results = chatbot.search_policies(
                            search_query, 
                            category=category_filter if category_filter != "None" else None,
                            doc_type=type_filter if type_filter != "None" else None,
                            limit=search_limit
                        )
                        
                        if results:
                            st.success(f"✅ Found {len(results)} relevant policies")
                            
                            # Display results in modern cards
                            for i, result in enumerate(results, 1):
                                confidence_color = "#10b981" if result['similarity'] >= 0.7 else "#f59e0b" if result['similarity'] >= 0.5 else "#ef4444"
                                
                                st.markdown(f"""
                                <div style="background: rgba(255,255,255,0.9); border-radius: 16px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 6px solid {confidence_color};">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                                        <h3 style="margin: 0; color: #1e293b;">{i}. {result['filename']}</h3>
                                        <span style="background: {confidence_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                                            {result['similarity']:.2f}
                                        </span>
                                    </div>
                                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                                        <div>
                                            <strong style="color: #64748b;">Category:</strong><br>
                                            <span style="color: #1e293b;">{result['category']}</span>
                                        </div>
                                        <div>
                                            <strong style="color: #64748b;">Type:</strong><br>
                                            <span style="color: #1e293b;">{result['document_type']}</span>
                                        </div>
                                    </div>
                                    <div>
                                        <strong style="color: #64748b;">Content Preview:</strong><br>
                                        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.9rem; line-height: 1.5;">
                                            {result['content'][:300]}{'...' if len(result['content']) > 300 else ''}
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("🔍 No policies found matching your search.")
                else:
                    st.warning("⚠️ Please enter a search query.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Policy summary
        st.subheader("📊 Policy Summary")
        if st.button("📈 Get Summary"):
            summary = chatbot.get_policy_summary()
            if "error" not in summary:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Policies", summary.get('total_policies', 0))
                with col2:
                    st.metric("Categories", len(summary.get('categories', {})))
                with col3:
                    st.metric("Document Types", len(summary.get('document_types', {})))
                
                # Display categories
                if summary.get('categories'):
                    st.write("**Policy Categories:**")
                    for category, count in summary['categories'].items():
                        st.write(f"• {category}: {count}")
            else:
                st.error(f"Error: {summary['error']}")
    
    # Analytics tab
    with tab3:
        st.header("📊 System Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Vector Store Stats")
            if st.button("📊 Get Stats"):
                stats = chatbot.vector_store.get_collection_stats()
                if stats:
                    st.metric("Total Documents", stats.get('total_documents', 0))
                    st.metric("Total Chunks", stats.get('total_chunks', 0))
                    st.metric("Embedding Model", stats.get('embedding_model', 'Unknown'))
                    
                    # Display chunking info
                    st.write(f"**Chunk Size:** {Config.CHUNK_SIZE}")
                    st.write(f"**Chunk Overlap:** {Config.CHUNK_OVERLAP}")
                else:
                    st.error("Could not retrieve stats")
        
        with col2:
            st.subheader("💰 Cost Analysis")
            if st.button("💵 Analyze Costs"):
                analysis = chatbot.get_cost_analysis()
                if "error" not in analysis:
                    st.metric("Total Requests", analysis.get('total_requests', 0))
                    st.metric("Total Tokens", analysis.get('total_tokens', 0))
                    st.metric("Avg Tokens", f"{analysis.get('average_tokens_per_request', 0):.1f}")
                    
                    # Display suggestions
                    if analysis.get('optimization_suggestions'):
                        st.write("**Suggestions:**")
                        for suggestion in analysis['optimization_suggestions']:
                            st.write(f"• {suggestion}")
                else:
                    st.error(f"Error: {analysis['error']}")
        
        # Cost optimization
        st.subheader("⚡ Cost Optimization")
        if st.button("🚀 Optimize for Cost"):
            with st.spinner("Analyzing optimization opportunities..."):
                optimization = chatbot.optimize_for_cost()
                if optimization.get('success'):
                    st.success(optimization['message'])
                    if optimization.get('suggestions'):
                        st.write("**Optimization Suggestions:**")
                        for suggestion in optimization['suggestions']:
                            st.write(f"• {suggestion}")
                else:
                    st.error(f"Error: {optimization['error']}")
    
    # Upload tab
    with tab4:
        st.header("📤 Upload New Policy Documents")
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.write("Upload new policy documents to add them to the knowledge base.")
        
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=Config.ALLOWED_EXTENSIONS,
            help=f"Supported formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Process the uploaded document
                with st.spinner("Processing uploaded document..."):
                    result = chatbot.upload_and_process_document(tmp_file_path, uploaded_file.name)
                    
                    if result.get('success'):
                        st.success(result['message'])
                        st.write(f"**Filename:** {result['filename']}")
                        st.write(f"**Chunks Added:** {result['chunks_added']}")
                        
                        # Display metadata
                        if result.get('metadata'):
                            st.write("**Metadata:**")
                            metadata = result['metadata']
                            st.write(f"• Category: {metadata.get('category', 'Unknown')}")
                            st.write(f"• Type: {metadata.get('document_type', 'Unknown')}")
                            st.write(f"• Date: {metadata.get('date', 'Unknown')}")
                    else:
                        st.error(f"Upload failed: {result.get('message', 'Unknown error')}")
                        if result.get('error'):
                            st.error(f"Error details: {result['error']}")
            
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Document list
        st.subheader("📋 Current Documents")
        if st.button("🔄 Refresh Document List"):
            documents = chatbot.get_document_list()
            if documents:
                for doc in documents:
                    st.write(f"**Total Documents:** {doc.get('total_documents', 0)}")
                    if doc.get('categories'):
                        st.write("**Categories:**")
                        for category, count in doc['categories'].items():
                            st.write(f"• {category}: {count}")
            else:
                st.info("No documents found.")
    
    # System Management Section
    st.markdown("### 🔧 System Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 System Status")
        if st.button("🔍 Check Status", use_container_width=True):
            with st.spinner("🔍 Checking system status..."):
                try:
                    stats = chatbot.vector_store.get_collection_stats()
                    if 'error' not in stats:
                        st.success(f"✅ {stats.get('total_documents', 0)} documents")
                        st.metric("Total Documents", stats.get('total_documents', 0))
                        st.metric("Total Chunks", stats.get('total_chunks', 0))
                    else:
                        st.error(f"❌ {stats['error']}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 📁 Document Management")
        if st.button("📂 Organize Docs", use_container_width=True):
            with st.spinner("📂 Organizing documents..."):
                try:
                    results = chatbot.process_and_index_documents()
                    if results.get('indexed_documents'):
                        st.success(f"✅ {len(results['indexed_documents'])} docs organized")
                    else:
                        st.error("❌ Organization failed")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 🧪 System Test")
        if st.button("🔍 Test Systems", use_container_width=True):
            with st.spinner("🧪 Testing systems..."):
                try:
                    test_results = chatbot.test_system()
                    if test_results["overall"]:
                        st.success("✅ All systems operational")
                    else:
                        st.error("❌ System issues detected")
                except Exception as e:
                    st.error(f"❌ Test failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom Prompts Management
    st.markdown("### 🎯 Custom Prompts Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### 📋 View Custom Prompts")
        if st.button("📋 View Prompts", use_container_width=True):
            try:
                prompts = chatbot.get_custom_prompts()
                if prompts.get('success'):
                    st.success(f"✅ {prompts['total_prompts']} custom prompts found")
                    for prompt_key, prompt_data in prompts['custom_prompts'].items():
                        with st.expander(f"📝 {prompt_key.replace('_', ' ').title()}"):
                            st.write("**Keywords:**")
                            for keyword in prompt_data['keywords']:
                                st.write(f"  • {keyword}")
                            st.write("**Response:**")
                            st.write(prompt_data['response'])
                else:
                    st.error(f"❌ Failed: {prompts.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("#### ➕ Add New Prompt")
        new_prompt_key = st.text_input("Prompt Key", key="new_prompt_key", placeholder="e.g., salary_policy")
        new_keywords = st.text_area("Keywords (one per line)", key="new_keywords", placeholder="salary\nincrement\npolicy")
        new_response = st.text_area("Response", key="new_response", placeholder="Enter the response text...")
        new_confidence = st.slider("Confidence", 0.1, 1.0, 0.9, key="new_confidence")
        
        if st.button("Add Prompt", use_container_width=True):
            if new_prompt_key and new_keywords and new_response:
                keywords_list = [k.strip() for k in new_keywords.split('\n') if k.strip()]
                result = chatbot.add_custom_prompt(new_prompt_key, keywords_list, new_response, new_confidence)
                
                if result.get('success'):
                    st.success(f"✅ {result['message']}")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.warning("⚠️ Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-logo">S</div>
        <p class="footer-text">Powered by Sysnova - Intelligent Solutions for Business</p>
        <p class="footer-text">© 2024 Kazi Farms Group. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Close main content container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 