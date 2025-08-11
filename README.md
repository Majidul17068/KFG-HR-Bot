# 🏢 KFG Policy Chatbot

An intelligent AI chatbot for KFG (Kazi Farms Group) policy documents using RAG (Retrieval-Augmented Generation) with DeepSeek models and ChromaDB vector database.

## 🚀 Features

- **📚 Document Processing**: Extract text from PDFs and images using OCR
- **🔍 Intelligent Search**: Vector-based document retrieval using ChromaDB
- **🤖 AI-Powered Responses**: Generate accurate answers using DeepSeek models
- **🌐 Bangla Translation**: Automatic translation of documents to Bangla
- **💬 Interactive Chat**: Modern Streamlit interface for easy interaction
- **📤 Document Upload**: Add new policy documents through the web interface
- **📊 Source Attribution**: See which documents were used to generate answers

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Documents     │    │  Document       │    │   Vector Store  │
│   (PDF/Images)  │───▶│  Processor      │───▶│   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   DeepSeek      │    │   Chatbot       │
│   Frontend      │◀───│   API Client    │◀───│   Engine        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- DeepSeek API key
- Tesseract OCR (for image processing)

### Install Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-ben
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd KFG_policy_chatbot
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp env_example.txt .env
# Edit .env and add your DeepSeek API key
```

4. **Create necessary directories:**
```bash
mkdir -p documents kfg_policy chroma_db
```

## ⚙️ Configuration

Edit the `.env` file with your settings:

```env
# Required
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Optional (defaults shown)
MODEL_NAME=deepseek-chat
TRANSLATE_TO_BANGLA=true
CHUNK_SIZE=1000
SIMILARITY_THRESHOLD=0.7
```

## 🚀 Usage

### 1. Process Existing Documents

First, process and index your existing policy documents:

```bash
python document_processor.py
python vector_store.py
```

### 2. Run the Chatbot

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### 3. Using the Interface

#### Chat Tab
- Ask questions about KFG policies in English or Bangla
- View source documents used for answers
- Clear chat history when needed

#### Upload Tab
- Upload new policy documents (PDF, PNG, JPG, TXT)
- Documents are automatically processed and indexed
- View processing results and statistics

#### Sidebar
- Test system components
- Process and index documents
- View document statistics

## 📁 Project Structure

```
KFG_policy_chatbot/
├── app.py                 # Main Streamlit application
├── chatbot.py             # Core chatbot logic
├── config.py              # Configuration settings
├── document_processor.py  # Document processing and OCR
├── vector_store.py        # ChromaDB vector store operations
├── deepseek_client.py     # DeepSeek API client
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # This file
├── documents/            # Original policy documents
├── kfg_policy/           # Processed text files
└── chroma_db/            # Vector database storage
```

## 🔧 API Reference

### KFGChatbot Class

```python
# Initialize chatbot
chatbot = KFGChatbot()

# Process and index documents
results = chatbot.process_and_index_documents()

# Chat with the bot
response = chatbot.chat("What is the TA-DA policy?")

# Upload new document
result = chatbot.upload_and_process_document("path/to/file.pdf", "filename.pdf")

# Test system
test_results = chatbot.test_system()
```

## 🎯 Best Practices

### 1. Document Quality
- Use high-quality PDFs for better text extraction
- Ensure images are clear for OCR processing
- Organize documents with descriptive filenames

### 2. Question Formulation
- Ask specific questions for better answers
- Include relevant keywords from policy documents
- Use both English and Bangla as needed

### 3. System Maintenance
- Regularly update the document index
- Monitor API usage and costs
- Backup the ChromaDB database

## 🔍 Troubleshooting

### Common Issues

1. **OCR not working:**
   - Ensure Tesseract is installed and in PATH
   - Install Bengali language pack: `tesseract-ocr-ben`

2. **DeepSeek API errors:**
   - Check API key is correct
   - Verify API quota and limits
   - Test connection using the system test

3. **Vector store issues:**
   - Clear and rebuild the database if needed
   - Check disk space for ChromaDB storage

4. **Document processing fails:**
   - Check file permissions
   - Verify supported file formats
   - Review error logs

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- DeepSeek for providing the AI models
- ChromaDB for the vector database
- Streamlit for the web interface
- Tesseract for OCR capabilities

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section

---

**Note:** This chatbot is designed specifically for KFG policy documents. Ensure all uploaded documents comply with your organization's data policies and security requirements. 