#!/usr/bin/env python3
"""
KFG Policy Chatbot - Main Entry Point
This file serves as the main entry point for the modular project structure
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Main entry point for the KFG Policy Chatbot"""
    print("🚀 KFG Policy Chatbot - Modular System")
    print("=" * 50)
    
    try:
        # Test imports
        from models.llm.deepseek_llm import DeepSeekLLMService
        from rag_engine.vector_store.vector_store import VectorStore
        from ui.terminal.chatbot import KFGChatbot
        from config.config import Config
        
        print("✅ All modules imported successfully!")
        print("✅ Modular structure is working correctly!")
        
        # Show available modules
        print("\n📁 Available Modules:")
        print("   • models/llm/ - DeepSeek LLM services")
        print("   • rag_engine/ - RAG and vector operations")
        print("   • ui/ - User interfaces (Streamlit & Terminal)")
        print("   • config/ - Configuration settings")
        print("   • utils/ - Helper functions and scripts")
        
        print("\n🎯 System is ready!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Please check the module structure and imports")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 