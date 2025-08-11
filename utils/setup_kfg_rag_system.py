#!/usr/bin/env python3
"""
KFG Policy RAG System - Complete Setup
Orchestrates the entire setup process from document processing to RAG system
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def print_step(step_num, total_steps, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}/{total_steps}: {description}")
    print("-" * 50)

def run_script(script_name, description):
    """Run a Python script and return success status"""
    print(f"   🔄 Running {script_name}...")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"   ✅ {description} completed successfully")
            if result.stdout:
                print(f"   📤 Output: {result.stdout[-200:]}...")  # Last 200 chars
            return True
        else:
            print(f"   ❌ {description} failed")
            if result.stderr:
                print(f"   📤 Error: {result.stderr[-200:]}...")  # Last 200 chars
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {description} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"   ❌ {description} failed with exception: {e}")
        return False

def check_prerequisites():
    """Check if all prerequisites are met"""
    print_header("Checking Prerequisites")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please create it with your DeepSeek API key")
        return False
    print("✅ .env file found")
    
    # Check if required folders exist
    required_folders = ['documents', 'kfg_policy']
    for folder in required_folders:
        if not os.path.exists(folder):
            print(f"❌ Required folder '{folder}' not found")
            return False
        print(f"✅ Folder '{folder}' found")
    
    # Check if kfg_policy has text files
    kfg_policy_path = 'kfg_policy'
    txt_files = [f for f in os.listdir(kfg_policy_path) if f.endswith('.txt')]
    if not txt_files:
        print("❌ No text files found in kfg_policy folder")
        return False
    print(f"✅ Found {len(txt_files)} text files in kfg_policy folder")
    
    return True

def main():
    """Main setup function"""
    print_header("KFG Policy RAG System - Complete Setup")
    print("This script will set up the complete RAG system for KFG policy documents")
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above and try again.")
        return
    
    # Confirm setup
    print("\n📋 Setup will perform the following steps:")
    print("1. Fix and process OCR-extracted KFG policy documents")
    print("2. Set up ChromaDB vector database")
    print("3. Test the RAG system")
    print("4. Launch the Streamlit chatbot interface")
    
    response = input("\nDo you want to continue with the setup? (y/N): ").strip().lower()
    if response != 'y':
        print("Setup cancelled.")
        return
    
    total_steps = 4
    current_step = 0
    
    # Step 1: Fix and process documents
    current_step += 1
    print_step(current_step, total_steps, "Fixing and Processing KFG Policy Documents")
    
    if not run_script('../rag_engine/document_processing/fix_kfg_documents.py', 'Document processing'):
        print("❌ Document processing failed. Cannot continue.")
        return
    
    # Step 2: Set up vector database
    current_step += 1
    print_step(current_step, total_steps, "Setting Up ChromaDB Vector Database")
    
    if not run_script('setup_vector_database.py', 'Vector database setup'):
        print("❌ Vector database setup failed. Cannot continue.")
        return
    
    # Step 3: Test RAG system
    current_step += 1
    print_step(current_step, total_steps, "Testing RAG System")
    
    if not run_script('test_rag_system.py', 'RAG system testing'):
        print("⚠️  RAG system testing failed, but continuing with setup...")
    
    # Step 4: Launch chatbot interface
    current_step += 1
    print_step(current_step, total_steps, "Launching Chatbot Interface")
    
    print("   🚀 Starting Streamlit chatbot interface...")
    print("   📱 The interface will open in your browser")
    print("   🔄 You can stop it anytime with Ctrl+C")
    
    try:
        # Launch Streamlit app
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', '../ui/streamlit/app.py'], 
                      timeout=3600)  # 1 hour timeout
    except KeyboardInterrupt:
        print("\n   ⏹️  Chatbot interface stopped by user")
    except subprocess.TimeoutExpired:
        print("\n   ⏰ Chatbot interface timed out")
    except Exception as e:
        print(f"\n   ❌ Failed to launch chatbot interface: {e}")
    
    # Final summary
    print_header("Setup Complete!")
    print("🎉 Your KFG Policy RAG system is now ready!")
    print("\n📁 What was created:")
    print("   • Cleaned and processed policy documents")
    print("   • ChromaDB vector database with embeddings")
    print("   • Document index and metadata")
    print("   • Bangla translations (if enabled)")
    
    print("\n🚀 How to use:")
    print("   • Run 'python app.py' to start the chatbot")
    print("   • Run 'python test_rag_system.py' to test the system")
    print("   • Upload new policy documents through the interface")
    
    print("\n📚 System features:")
    print("   • Multi-language support (English/Bangla)")
    print("   • Cost monitoring and optimization")
    print("   • Document upload and processing")
    print("   • RAG-based accurate policy answers")
    
    print("\n💡 Next steps:")
    print("   • Test with various policy questions")
    print("   • Upload additional policy documents")
    print("   • Customize the system as needed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        print("Please check the error messages above and try again.") 