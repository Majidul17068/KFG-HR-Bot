#!/usr/bin/env python3
"""
Test script for KFG Policy Chatbot
"""

import os
import sys
import logging
from ..config.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    try:
        print(f"✅ DeepSeek API Key: {'Set' if Config.DEEPSEEK_API_KEY else 'Not set'}")
        print(f"✅ Model: {Config.MODEL_NAME}")
        print(f"✅ Vector DB Path: {Config.CHROMA_DB_PATH}")
        print(f"✅ Documents Path: {Config.DOCUMENTS_PATH}")
        print(f"✅ Extracted Path: {Config.EXTRACTED_PATH}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_document_processor():
    """Test document processor"""
    print("\n📄 Testing document processor...")
    try:
        from ..rag_engine.document_processing.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("✅ Document processor initialized")
        
        # Test text cleaning
        test_text = "This is a test document with some formatting issues.   Multiple spaces   and special chars!@#"
        cleaned = processor.clean_text(test_text)
        print(f"✅ Text cleaning works: {len(cleaned)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Document processor error: {e}")
        return False

def test_vector_store():
    """Test vector store"""
    print("\n🗄️ Testing vector store...")
    try:
        from ..rag_engine.vector_store.vector_store import VectorStore
        vector_store = VectorStore()
        print("✅ Vector store initialized")
        
        # Test collection stats
        stats = vector_store.get_collection_stats()
        print(f"✅ Collection stats: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Vector store error: {e}")
        return False

def test_deepseek_client():
    """Test DeepSeek client"""
    print("\n🤖 Testing DeepSeek client...")
    try:
        from ..models.llm.deepseek_client import DeepSeekClient
        client = DeepSeekClient()
        print("✅ DeepSeek client initialized")
        
        # Test connection
        if client.test_connection():
            print("✅ DeepSeek API connection successful")
        else:
            print("❌ DeepSeek API connection failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ DeepSeek client error: {e}")
        return False

def test_chatbot():
    """Test main chatbot"""
    print("\n💬 Testing chatbot...")
    try:
        from ..ui.terminal.chatbot import KFGChatbot
        chatbot = KFGChatbot()
        print("✅ Chatbot initialized")
        
        # Test system
        test_results = chatbot.test_system()
        print(f"✅ System test results: {test_results}")
        
        return test_results["overall"]
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return False

def test_directories():
    """Test directory structure"""
    print("\n📁 Testing directory structure...")
    required_dirs = [
        Config.DOCUMENTS_PATH,
        Config.EXTRACTED_PATH,
        Config.CHROMA_DB_PATH
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Directory missing: {directory}")
            all_exist = False
    
    return all_exist

def test_sample_documents():
    """Test with sample documents if available"""
    print("\n📚 Testing sample documents...")
    
    # Check if there are documents to process
    if os.path.exists(Config.DOCUMENTS_PATH):
        doc_files = [f for f in os.listdir(Config.DOCUMENTS_PATH) 
                    if f.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg', '.txt'))]
        
        if doc_files:
            print(f"✅ Found {len(doc_files)} documents in {Config.DOCUMENTS_PATH}")
            
            # Check if extracted files exist
            if os.path.exists(Config.EXTRACTED_PATH):
                extracted_files = [f for f in os.listdir(Config.EXTRACTED_PATH) 
                                 if f.lower().endswith('.txt')]
                print(f"✅ Found {len(extracted_files)} extracted files in {Config.EXTRACTED_PATH}")
            else:
                print("⚠️  No extracted files found - run document processing first")
        else:
            print("⚠️  No documents found in documents folder")
    else:
        print("⚠️  Documents directory not found")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Running KFG Policy Chatbot System Tests")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_config),
        ("Directory Structure", test_directories),
        ("Document Processor", test_document_processor),
        ("Vector Store", test_vector_store),
        ("DeepSeek Client", test_deepseek_client),
        ("Chatbot", test_chatbot),
        ("Sample Documents", test_sample_documents),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Add your DeepSeek API key to .env file")
        print("2. Place policy documents in the 'documents' folder")
        print("3. Run: python document_processor.py")
        print("4. Run: python vector_store.py")
        print("5. Start the app: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Install Tesseract OCR for your system")
        print("- Set your DeepSeek API key in .env file")
        print("- Check file permissions and directory access")

if __name__ == "__main__":
    main() 