#!/usr/bin/env python3
"""
Quick Start Script for KFG Policy Chatbot
This script provides a fast way to get the system running
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the startup banner"""
    print("🏢" + "="*60 + "🏢")
    print("🚀 KFG Policy Chatbot - Quick Start")
    print("🏢" + "="*60 + "🏢")
    print()

def check_environment():
    """Check and setup environment"""
    print("🔍 Checking environment...")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        if os.path.exists("env_example.txt"):
            print("📝 Creating .env file from template...")
            try:
                with open("env_example.txt", "r") as f:
                    template = f.read()
                
                with open(".env", "w") as f:
                    f.write(template)
                
                print("⚠️  Please edit .env file and add your DeepSeek API key!")
                print("   Then run this script again.")
                return False
            except Exception as e:
                print(f"❌ Error creating .env: {e}")
                return False
        else:
            print("❌ No .env file or env_example.txt found!")
            return False
    
    # Check if kfg_policy folder exists
    if not os.path.exists("./kfg_policy"):
        print("❌ kfg_policy folder not found!")
        print("   Please ensure you have extracted policy documents in the kfg_policy folder")
        return False
    
    print("✅ Environment check passed!")
    return True

def run_setup():
    """Run the enhanced setup"""
    print("\n🔄 Running enhanced setup...")
    
    try:
        # Run the enhanced setup script
        result = subprocess.run([sys.executable, "../utils/setup_enhanced_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Setup completed successfully!")
            return True
        else:
            print("❌ Setup failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running setup: {e}")
        return False

def start_chatbot():
    """Start the Streamlit chatbot"""
    print("\n🚀 Starting KFG Policy Chatbot...")
    print("   The application will open in your browser.")
    print("   Press Ctrl+C to stop the chatbot.")
    print()
    
    try:
        # Start Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Chatbot stopped by user.")
    except Exception as e:
        print(f"❌ Error starting chatbot: {e}")

def show_help():
    """Show help information"""
    print("\n📚 Quick Start Guide:")
    print("=" * 50)
    print("1. Ensure you have policy documents in the kfg_policy folder")
    print("2. Set your DeepSeek API key in the .env file")
    print("3. Run this script to setup and start the system")
    print()
    print("📁 File Structure:")
    print("   kfg_policy/           - Your policy documents")
    print("   .env                  - API configuration")
    print("   app.py                - Main Streamlit application")
    print("   chatbot.py            - Core chatbot logic")
    print("   vector_store.py       - ChromaDB integration")
    print()
    print("🔧 Manual Setup:")
    print("   python setup_enhanced_system.py  - Full setup")
    print("   python fix_kfg_documents.py      - Document organization only")
    print("   streamlit run app.py             - Start chatbot directly")
    print()
    print("📞 Support:")
    print("   Check the README.md for detailed information")
    print("   Review logs for troubleshooting")

def main():
    """Main quick start function"""
    print_banner()
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup failed!")
        show_help()
        return
    
    # Ask user what they want to do
    print("\n🎯 What would you like to do?")
    print("1. 🚀 Quick Setup & Start (Recommended)")
    print("2. 🔧 Setup Only")
    print("3. 🚀 Start Chatbot Only (if already setup)")
    print("4. 📚 Show Help")
    print("5. ❌ Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                # Quick setup and start
                if run_setup():
                    start_chatbot()
                break
                
            elif choice == "2":
                # Setup only
                run_setup()
                break
                
            elif choice == "3":
                # Start chatbot only
                start_chatbot()
                break
                
            elif choice == "4":
                # Show help
                show_help()
                break
                
            elif choice == "5":
                # Exit
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    main() 