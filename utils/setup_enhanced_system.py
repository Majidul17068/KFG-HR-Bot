#!/usr/bin/env python3
"""
Enhanced KFG Policy Chatbot Setup Script
This script will:
1. Organize and categorize all policy documents
2. Create comprehensive metadata
3. Rebuild the vector database index
4. Test the system
"""

import os
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('setup_enhanced_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def check_prerequisites():
    """Check if all prerequisites are met"""
    logger.info("Checking prerequisites...")
    
    # Check if kfg_policy folder exists
    if not os.path.exists("./kfg_policy"):
        logger.error("❌ kfg_policy folder not found!")
        logger.error("Please ensure you have extracted policy documents in the kfg_policy folder")
        return False
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        logger.warning("⚠️  .env file not found. Please create one with your DeepSeek API key")
        logger.info("You can copy env_example.txt to .env and add your API key")
    
    # Check Python packages
    try:
        import chromadb
        import sentence_transformers
        import streamlit
        import requests
        logger.info("✅ All required Python packages are available")
    except ImportError as e:
        logger.error(f"❌ Missing required package: {e}")
        logger.error("Please run: pip install -r requirements.txt")
        return False
    
    return True

def run_document_organization():
    """Run the document organization process"""
    logger.info("🔄 Starting document organization...")
    
    try:
        from ..rag_engine.document_processing.fix_kfg_documents import KFGDocumentFixer
        
        fixer = KFGDocumentFixer()
        results = fixer.process_all_documents()
        index = fixer.create_index_file()
        
        logger.info("✅ Document organization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Document organization failed: {e}")
        return False

def rebuild_vector_index():
    """Rebuild the vector database index"""
    logger.info("🔄 Rebuilding vector database index...")
    
    try:
        from ..rag_engine.vector_store.vector_store import VectorStore
        
        vector_store = VectorStore()
        added_docs = vector_store.rebuild_index()
        
        if added_docs:
            logger.info(f"✅ Vector index rebuilt with {len(added_docs)} documents")
            return True
        else:
            logger.error("❌ No documents were added to the vector index")
            return False
            
    except Exception as e:
        logger.error(f"❌ Vector index rebuild failed: {e}")
        return False

def test_system():
    """Test the enhanced system"""
    logger.info("🧪 Testing the enhanced system...")
    
    try:
        from ..ui.terminal.chatbot import KFGChatbot
        
        chatbot = KFGChatbot()
        
        # Test basic functionality
        test_results = chatbot.test_system()
        
        if test_results.get('status') == 'success':
            logger.info("✅ System test passed")
            return True
        else:
            logger.error(f"❌ System test failed: {test_results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ System test failed: {e}")
        return False

def show_system_status():
    """Show the current system status"""
    logger.info("📊 System Status Report")
    logger.info("=" * 50)
    
    try:
        from vector_store import VectorStore
        from chatbot import KFGChatbot
        
        # Get vector store stats
        vector_store = VectorStore()
        stats = vector_store.get_collection_stats()
        
        if 'error' not in stats:
            logger.info(f"Vector Database: {stats['collection_name']}")
            logger.info(f"Total Documents: {stats['total_documents']}")
            logger.info(f"Categories: {len(stats.get('categories', {}))}")
            logger.info(f"Document Types: {len(stats.get('document_types', {}))}")
        else:
            logger.error(f"Vector store error: {stats['error']}")
        
        # Get chatbot info
        chatbot = KFGChatbot()
        policy_categories = chatbot.get_policy_categories()
        document_types = chatbot.get_document_types()
        
        logger.info(f"Policy Categories: {len(policy_categories)}")
        logger.info(f"Document Types: {len(document_types)}")
        
        # Show organized documents
        organized_path = Path("./kfg_policy/organized")
        if organized_path.exists():
            organized_files = list(organized_path.glob("*.txt"))
            logger.info(f"Organized Documents: {len(organized_files)}")
        
        # Show metadata files
        metadata_path = Path("./kfg_policy/metadata")
        if metadata_path.exists():
            metadata_files = list(metadata_path.glob("*.json"))
            logger.info(f"Metadata Files: {len(metadata_files)}")
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")

def main():
    """Main setup function"""
    print("🚀 Enhanced KFG Policy Chatbot Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Setup cannot continue. Please fix the issues above.")
        return
    
    print("\n✅ Prerequisites check passed!")
    
    # Step 1: Organize documents
    print("\n📁 Step 1: Organizing documents...")
    if not run_document_organization():
        print("❌ Document organization failed. Setup cannot continue.")
        return
    
    # Step 2: Rebuild vector index
    print("\n🔍 Step 2: Rebuilding vector index...")
    if not rebuild_vector_index():
        print("❌ Vector index rebuild failed. Setup cannot continue.")
        return
    
    # Step 3: Test system
    print("\n🧪 Step 3: Testing system...")
    if not test_system():
        print("❌ System test failed. Please check the logs.")
        return
    
    # Show final status
    print("\n🎉 Setup completed successfully!")
    show_system_status()
    
    print("\n" + "=" * 50)
    print("🚀 Your enhanced KFG Policy Chatbot is ready!")
    print("\nTo start the chatbot:")
    print("  streamlit run app.py")
    print("\nTo test the system:")
    print("  python test_system.py")
    print("\nFor quick setup:")
    print("  python quick_start.py")
    print("=" * 50)

if __name__ == "__main__":
    main() 