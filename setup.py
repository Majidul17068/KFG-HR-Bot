#!/usr/bin/env python3
"""
Setup script for KFG Policy Chatbot
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def check_tesseract():
    """Check if Tesseract is installed"""
    print("🔍 Checking Tesseract installation...")
    try:
        result = subprocess.run(["tesseract", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract is installed")
            return True
        else:
            print("❌ Tesseract not found")
            return False
    except FileNotFoundError:
        print("❌ Tesseract not found")
        return False

def install_tesseract():
    """Install Tesseract based on the operating system"""
    system = platform.system().lower()
    
    print(f"🔧 Installing Tesseract for {system}...")
    
    if system == "linux":
        try:
            # Try to detect the distribution
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    subprocess.check_call(["sudo", "apt", "update"])
                    subprocess.check_call(["sudo", "apt", "install", "-y", "tesseract-ocr", "tesseract-ocr-ben"])
                elif "fedora" in content or "rhel" in content or "centos" in content:
                    subprocess.check_call(["sudo", "dnf", "install", "-y", "tesseract", "tesseract-langpack-ben"])
                else:
                    print("⚠️  Please install Tesseract manually for your Linux distribution")
                    return False
            print("✅ Tesseract installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Tesseract: {e}")
            return False
    
    elif system == "darwin":  # macOS
        try:
            subprocess.check_call(["brew", "install", "tesseract", "tesseract-lang"])
            print("✅ Tesseract installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Tesseract: {e}")
            print("💡 Make sure Homebrew is installed: https://brew.sh/")
            return False
    
    elif system == "windows":
        print("⚠️  Please install Tesseract manually from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    
    else:
        print(f"⚠️  Unsupported operating system: {system}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ["documents", "kfg_policy", "chroma_db"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory already exists: {directory}")

def setup_environment():
    """Set up environment file"""
    print("⚙️  Setting up environment...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env_example.txt"):
            with open("env_example.txt", "r") as f:
                content = f.read()
            
            with open(".env", "w") as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your DeepSeek API key")
        else:
            print("⚠️  env_example.txt not found, creating basic .env file")
            with open(".env", "w") as f:
                f.write("DEEPSEEK_API_KEY=your_deepseek_api_key_here\n")
    else:
        print("✅ .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up KFG Policy Chatbot...")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install Python dependencies
    install_dependencies()
    
    # Check and install Tesseract
    if not check_tesseract():
        print("🔧 Tesseract not found, attempting to install...")
        if not install_tesseract():
            print("⚠️  Tesseract installation failed. Please install manually.")
            print("   Ubuntu/Debian: sudo apt install tesseract-ocr tesseract-ocr-ben")
            print("   macOS: brew install tesseract tesseract-lang")
            print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your DeepSeek API key")
    print("2. Place your policy documents in the 'documents' folder")
    print("3. Run: python document_processor.py")
    print("4. Run: python vector_store.py")
    print("5. Start the app: streamlit run app.py")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 