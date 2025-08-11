#!/usr/bin/env python3
"""
KFG Policy Vector Database Setup
Creates and populates ChromaDB with processed policy documents
"""

import os
import json
from pathlib import Path
from ..config.config import Config
from ..rag_engine.vector_store.vector_store import VectorStore
from ..rag_engine.document_processing.document_processor import DocumentProcessor

def main():
    print("🗄️  KFG Policy Vector Database Setup")
    print("=" * 50)
    
    # Check if cleaned documents exist
    cleaned_docs_path = os.path.join(Config.EXTRACTED_PATH, 'cleaned_documents')
    if not os.path.exists(cleaned_docs_path):
        print(f"❌ Cleaned documents folder not found: {cleaned_docs_path}")
        print("   Please run fix_kfg_documents.py first to process the documents")
        return
    
    # Initialize vector store
    try:
        vector_store = VectorStore()
        print("✅ Vector store initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize vector store: {e}")
        return
    
    # Check if database already has documents
    if vector_store.collection.count() > 0:
        print(f"⚠️  Database already contains {vector_store.collection.count()} documents")
        response = input("Do you want to clear and rebuild? (y/N): ").strip().lower()
        if response == 'y':
            print("🗑️  Clearing existing database...")
            vector_store.clear_database()
        else:
            print("📊 Using existing database")
            show_database_status(vector_store)
            return
    
    # Load document index
    index_file = os.path.join(Config.EXTRACTED_PATH, 'document_index.json')
    if not os.path.exists(index_file):
        print(f"❌ Document index not found: {index_file}")
        return
    
    with open(index_file, 'r', encoding='utf-8') as f:
        document_index = json.load(f)
    
    print(f"📚 Found {document_index['total_documents']} documents to process")
    
    # Process and add documents to vector database
    print("\n🔄 Adding documents to vector database...")
    
    added_count = 0
    failed_count = 0
    
    # Get list of cleaned document files
    cleaned_files = [f for f in os.listdir(cleaned_docs_path) if f.endswith('_cleaned.txt')]
    
    for cleaned_file in cleaned_files:
        try:
            base_name = cleaned_file.replace('_cleaned.txt', '')
            
            # Load cleaned text
            cleaned_path = os.path.join(cleaned_docs_path, cleaned_file)
            with open(cleaned_path, 'r', encoding='utf-8') as f:
                cleaned_text = f.read()
            
            # Load metadata
            metadata_path = os.path.join(cleaned_docs_path, f"{base_name}_metadata.json")
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            else:
                metadata = {'filename': base_name}
            
            # Load Bangla version if available
            bangla_path = os.path.join(cleaned_docs_path, f"{base_name}_bangla.txt")
            bangla_text = ""
            if os.path.exists(bangla_path):
                with open(bangla_path, 'r', encoding='utf-8') as f:
                    bangla_text = f.read()
            
            # Prepare document for vector store
            document_data = {
                'text': cleaned_text,
                'metadata': {
                    'filename': metadata.get('filename', base_name),
                    'document_type': metadata.get('document_type', 'Unknown'),
                    'policy_name': metadata.get('policy_name', ''),
                    'document_number': metadata.get('document_number', ''),
                    'date': metadata.get('date', ''),
                    'company_name': metadata.get('company_name', ''),
                    'language': 'English'
                }
            }
            
            # Add to vector store
            vector_store.add_document(document_data)
            added_count += 1
            
            print(f"   ✅ Added: {base_name}")
            
            # Add Bangla version if available
            if bangla_text:
                bangla_document = {
                    'text': bangla_text,
                    'metadata': {
                        'filename': f"{base_name}_bangla",
                        'document_type': metadata.get('document_type', 'Unknown'),
                        'policy_name': metadata.get('policy_name', ''),
                        'document_number': metadata.get('document_number', ''),
                        'date': metadata.get('date', ''),
                        'company_name': metadata.get('company_name', ''),
                        'language': 'Bangla',
                        'original_file': base_name
                    }
                }
                
                vector_store.add_document(bangla_document)
                added_count += 1
                print(f"   ✅ Added: {base_name} (Bangla)")
            
        except Exception as e:
            print(f"   ❌ Failed to add {cleaned_file}: {e}")
            failed_count += 1
    
    print(f"\n📊 Vector Database Setup Summary:")
    print(f"   Successfully added: {added_count} documents")
    print(f"   Failed: {failed_count} documents")
    print(f"   Total in database: {vector_store.collection.count()}")
    
    # Show database status
    show_database_status(vector_store)
    
    # Test search functionality
    print("\n🔍 Testing search functionality...")
    test_search_queries(vector_store)
    
    print("\n🎉 Vector database setup completed!")
    print("📚 Ready for RAG chatbot queries")

def show_database_status(vector_store):
    """Show current database status"""
    print(f"\n📊 Database Status:")
    print(f"   Total documents: {vector_store.collection.count()}")
    
    # Get unique document types
    results = vector_store.collection.get()
    if results and results['metadatas']:
        doc_types = set()
        languages = set()
        companies = set()
        
        for metadata in results['metadatas']:
            if metadata:
                doc_types.add(metadata.get('document_type', 'Unknown'))
                languages.add(metadata.get('language', 'Unknown'))
                companies.add(metadata.get('company_name', 'Unknown'))
        
        print(f"   Document types: {len(doc_types)}")
        print(f"   Languages: {', '.join(sorted(languages))}")
        print(f"   Companies: {len(companies)}")

def test_search_queries(vector_store):
    """Test search functionality with sample queries"""
    test_queries = [
        "TA-DA policy",
        "salary increment",
        "leave procedure",
        "medical bill policy",
        "uniform policy"
    ]
    
    print("   Testing sample queries:")
    for query in test_queries:
        try:
            results = vector_store.search(query, n_results=2)
            if results:
                print(f"   ✅ '{query}': Found {len(results)} results")
            else:
                print(f"   ⚠️  '{query}': No results found")
        except Exception as e:
            print(f"   ❌ '{query}': Search failed - {e}")

if __name__ == "__main__":
    main() 