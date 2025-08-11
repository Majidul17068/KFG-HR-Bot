#!/bin/bash

# 🚀 KFG Policy Chatbot - Automated Setup for New Policy Files
# =============================================================

echo "🚀 Starting KFG Policy Chatbot Setup with New Policy Files..."
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the KFG_policy_chatbot directory"
    exit 1
fi

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Please create one first:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if new policy files exist
if [ ! -d "kfg_policy/raw" ] || [ -z "$(ls -A kfg_policy/raw 2>/dev/null)" ]; then
    echo "⚠️  No policy files found in kfg_policy/raw/"
    echo "   Please place your .txt policy files in kfg_policy/raw/ folder first"
    exit 1
fi

echo "📁 Found policy files in kfg_policy/raw/"
echo "📊 Processing new policy files..."

# Step 1: Process and organize documents
echo "🔧 Step 1: Processing and organizing documents..."
python document_processor.py

# Step 2: Extract text from documents
echo "📝 Step 2: Extracting text from documents..."
python fix_kfg_documents.py

# Step 3: Set up enhanced RAG system
echo "🚀 Step 3: Setting up enhanced RAG system..."
python setup_enhanced_system.py

# Step 4: Build vector database
echo "🗄️  Step 4: Building vector database..."
python setup_vector_database.py

# Step 5: Test the system
echo "🧪 Step 5: Testing the system..."
python test_rag_system.py

echo ""
echo "🎉 Setup completed successfully!"
echo "============================================================"
echo "🚀 Starting the Streamlit application..."
echo "   The chatbot will open in your web browser"
echo "   Press Ctrl+C to stop the application"
echo ""

# Start the Streamlit application
streamlit run app.py 