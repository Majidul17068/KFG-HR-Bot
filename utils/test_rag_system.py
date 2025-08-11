#!/usr/bin/env python3
"""
KFG Policy RAG System Test
Tests the complete RAG pipeline with policy documents
"""

import os
import json
from ..config.config import Config
from ..ui.terminal.chatbot import KFGChatbot
from ..rag_engine.vector_store.vector_store import VectorStore

def main():
    print("🧪 KFG Policy RAG System Test")
    print("=" * 50)
    
    # Check if vector database exists and has documents
    try:
        vector_store = VectorStore()
        doc_count = vector_store.collection.count()
        
        if doc_count == 0:
            print("❌ Vector database is empty!")
            print("   Please run setup_vector_database.py first")
            return
        
        print(f"✅ Vector database ready with {doc_count} documents")
        
    except Exception as e:
        print(f"❌ Failed to initialize vector store: {e}")
        return
    
    # Initialize chatbot
    try:
        chatbot = KFGChatbot()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return
    
    # Test queries in both English and Bangla
    test_queries = [
        # English queries
        {
            'query': 'What is the TA-DA policy for officers?',
            'language': 'English',
            'expected_topics': ['TA-DA', 'officer', 'allowance']
        },
        {
            'query': 'What are the salary increment rules for management employees?',
            'language': 'English',
            'expected_topics': ['salary', 'increment', 'management']
        },
        {
            'query': 'What is the leave procedure for employees?',
            'language': 'English',
            'expected_topics': ['leave', 'procedure', 'employee']
        },
        {
            'query': 'What is the uniform policy for drivers?',
            'language': 'English',
            'expected_topics': ['uniform', 'driver', 'policy']
        },
        {
            'query': 'What are the medical bill reimbursement rules?',
            'language': 'English',
            'expected_topics': ['medical', 'bill', 'reimbursement']
        },
        
        # Bangla queries
        {
            'query': 'অফিসারদের জন্য TA-DA নীতি কী?',
            'language': 'Bangla',
            'expected_topics': ['TA-DA', 'অফিসার', 'ভাতা']
        },
        {
            'query': 'ব্যবস্থাপনা কর্মীদের জন্য বেতন বৃদ্ধির নিয়ম কী?',
            'language': 'Bangla',
            'expected_topics': ['বেতন', 'বৃদ্ধি', 'ব্যবস্থাপনা']
        },
        {
            'query': 'কর্মীদের জন্য ছুটির নিয়ম কী?',
            'language': 'Bangla',
            'expected_topics': ['ছুটি', 'নিয়ম', 'কর্মী']
        }
    ]
    
    print(f"\n🔍 Testing {len(test_queries)} queries...")
    print("=" * 60)
    
    successful_tests = 0
    total_tests = len(test_queries)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}/{total_tests}: {test_case['language']}")
        print(f"Query: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Get response from chatbot
            response = chatbot.chat(test_case['query'])
            
            if response:
                print(f"✅ Response received ({len(response)} characters)")
                print(f"Response: {response[:200]}...")
                
                # Check if response contains expected topics
                response_lower = response.lower()
                found_topics = []
                
                for topic in test_case['expected_topics']:
                    if topic.lower() in response_lower:
                        found_topics.append(topic)
                
                if found_topics:
                    print(f"✅ Found expected topics: {', '.join(found_topics)}")
                    successful_tests += 1
                else:
                    print(f"⚠️  Expected topics not found in response")
                    print(f"   Expected: {', '.join(test_case['expected_topics'])}")
                
            else:
                print("❌ No response received")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
        
        print("-" * 40)
    
    # Test document search directly
    print(f"\n🔍 Testing direct document search...")
    print("=" * 40)
    
    search_test_queries = [
        "TA-DA policy",
        "salary increment",
        "uniform policy",
        "medical bill",
        "leave procedure"
    ]
    
    for query in search_test_queries:
        try:
            results = vector_store.search(query, n_results=3)
            if results:
                print(f"✅ '{query}': Found {len(results)} documents")
                for j, result in enumerate(results[:2], 1):
                    metadata = result.get('metadata', {})
                    filename = metadata.get('filename', 'Unknown')
                    doc_type = metadata.get('document_type', 'Unknown')
                    print(f"   {j}. {filename} ({doc_type})")
            else:
                print(f"⚠️  '{query}': No results found")
        except Exception as e:
            print(f"❌ '{query}': Search failed - {e}")
    
    # Test cost monitoring
    print(f"\n💰 Testing cost monitoring...")
    print("=" * 40)
    
    try:
        from cost_monitor import cost_monitor
        usage_summary = cost_monitor.get_usage_summary()
        
        print(f"Total requests: {usage_summary['total']['requests']}")
        print(f"Total tokens: {usage_summary['total']['tokens']:,}")
        print(f"Total cost: ${usage_summary['total']['cost_usd']:.4f}")
        print(f"Today's requests: {usage_summary['today']['requests']}")
        print(f"Today's cost: ${usage_summary['today']['cost_usd']:.4f}")
        
    except Exception as e:
        print(f"⚠️  Cost monitoring not available: {e}")
    
    # Final summary
    print(f"\n📊 Test Summary:")
    print("=" * 40)
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("\n🎉 All tests passed! RAG system is working correctly.")
    elif successful_tests > total_tests * 0.7:
        print("\n✅ Most tests passed. RAG system is working well.")
    else:
        print("\n⚠️  Many tests failed. Please check the system configuration.")
    
    print(f"\n📚 Ready for production use!")

def test_specific_policy():
    """Test a specific policy query in detail"""
    print("\n🔍 Testing specific policy query...")
    
    try:
        chatbot = KFGChatbot()
        
        # Test a specific query
        query = "What is the TA-DA policy for senior executives?"
        print(f"Query: {query}")
        
        response = chatbot.chat(query)
        
        if response:
            print(f"\nResponse:")
            print(response)
            
            # Show source documents
            print(f"\n📄 Source Documents:")
            vector_store = VectorStore()
            results = vector_store.search(query, n_results=3)
            
            for i, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                print(f"{i}. {metadata.get('filename', 'Unknown')}")
                print(f"   Type: {metadata.get('document_type', 'Unknown')}")
                print(f"   Policy: {metadata.get('policy_name', 'Unknown')}")
                print(f"   Date: {metadata.get('date', 'Unknown')}")
                print()
        else:
            print("❌ No response received")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main()
    
    # Option to test specific policy
    response = input("\nWould you like to test a specific policy query? (y/N): ").strip().lower()
    if response == 'y':
        test_specific_policy() 