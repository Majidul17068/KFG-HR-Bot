#!/usr/bin/env python3
"""
Simple demo of custom prompt functionality
Shows how to use custom prompts for exact control over responses
"""

from ..models.llm.deepseek_llm import DeepSeekLLMService
from ..rag_engine.vector_store.vector_store import VectorStore

def demo_custom_prompts():
    """Demonstrate custom prompt functionality"""
    
    print("🎯 Custom Prompt Demo - EXACT Control Over Responses")
    print("=" * 60)
    
    try:
        # Initialize services
        llm_service = DeepSeekLLMService()
        vector_store = VectorStore()
        
        # Test a medical query
        query = "What is the medical bill coverage for employees?"
        print(f"🔍 Query: {query}")
        
        # Get relevant documents
        relevant_docs = vector_store.search(query, n_results=2)
        
        if relevant_docs:
            print(f"📚 Found {len(relevant_docs)} relevant documents")
            
            # Show the custom prompt being used
            custom_prompt = llm_service.get_custom_prompt_for_query_type("medical")
            print(f"\n📝 Custom Prompt (First 200 chars):")
            print(f"   {custom_prompt[:200]}...")
            
            # Process with custom prompt
            print(f"\n⚙️ Processing with custom prompt...")
            response = llm_service.process_query_with_custom_prompt(query, relevant_docs)
            
            print(f"✅ Response generated successfully!")
            print(f"   Length: {len(response)} characters")
            print(f"\n📋 Response Preview:")
            print("-" * 40)
            print(response[:500] + "..." if len(response) > 500 else response)
            print("-" * 40)
            
            # Check structure
            if "Medical Policy Response" in response:
                print("   ✅ Follows medical policy structure")
            else:
                print("   ⚠️ Structure verification needed")
        
        else:
            print("❌ No relevant documents found")
        
        print("\n✅ Custom prompt demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")

def demo_adding_custom_type():
    """Demonstrate adding a custom query type"""
    
    print("\n🔧 Adding Custom Query Type Demo")
    print("=" * 60)
    
    try:
        llm_service = DeepSeekLLMService()
        
        # Add a custom query type
        print("➕ Adding custom query type...")
        llm_service.add_custom_query_type(
            query_type="bonus_policy",
            patterns=[r"bonus", r"incentive", r"reward"],
            prompt_example="""You are an expert in KFG bonus and incentive policy analysis.

Your task is to generate a bonus policy response based on the provided documents.

The response must include:
1. **Bonus Policy Title**: Use exact terms from documents
2. **Bonus Types**: List all bonus categories mentioned
3. **Eligibility**: Who qualifies for bonuses
4. **Calculation**: How bonuses are calculated
5. **Payment Terms**: When and how bonuses are paid
6. **Source Documents**: Reference the documents used

Use only information explicitly stated in the documents."""
        )
        
        print("   ✅ Custom query type added!")
        
        # List all available types
        print(f"\n📋 Available Query Types:")
        query_types = llm_service.list_available_query_types()
        for qt in query_types:
            print(f"   • {qt}")
        
        print("\n✅ Custom type demo completed!")
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")

if __name__ == "__main__":
    print("🧪 Custom Prompt Functionality Demo")
    print("=" * 80)
    
    # Run demos
    demo_custom_prompts()
    demo_adding_custom_type()
    
    print("\n🎉 All demos completed!") 