# 🎯 Custom Prompt System for KFG Policy Chatbot

## 🚀 **EXACT Control Over Response Formats - Just Like Your Incident Report Example!**

This system gives you **precise control** over how each type of policy query is answered, using custom prompts that define exactly what the response should look like.

## 🎯 **What You Can Control**

### **1. 🏥 Medical Policy Queries**
**Patterns Detected:** `medical bill`, `medical coverage`, `health benefits`, `hospitalization`, `treatment`

**Custom Prompt Example:**
```
You are an expert in KFG medical policy analysis. Your task is to generate a comprehensive medical policy response based on the provided policy documents.

The response must be structured as follows:

1. **Medical Policy Response**: Provide a clear, concise title using the exact policy terms from the documents.
2. **Coverage Summary**: Craft a detailed explanation of what medical expenses are covered...
3. **Eligibility Criteria**: Describe who is eligible for medical benefits...
4. **Limits and Amounts**: Extract and present specific monetary limits...
5. **Required Procedures**: Detail the process for claiming medical benefits...
6. **Source Documents**: List the specific policy documents used...

Ensure that no information is inferred or added that is not explicitly stated in the policy documents.
```

### **2. 💰 Salary Policy Queries**
**Patterns Detected:** `salary increment`, `yearly increment`, `salary structure`, `compensation`, `bonus`

**Custom Prompt Example:**
```
You are an expert in KFG salary and compensation policy analysis...

The response must be structured as follows:

1. **Salary Policy Response**: Provide a clear, concise title...
2. **Increment Structure**: Detail the salary increment system...
3. **Eligibility Criteria**: Describe who is eligible...
4. **Effective Dates**: Specify when salary increments take effect...
5. **Additional Benefits**: List any supplementary compensation elements...
6. **Source Documents**: List the specific policy documents used...

Focus on extracting specific figures, percentages, and criteria directly from the policy documents.
```

### **3. 📅 Leave Policy Queries**
**Patterns Detected:** `leave policy`, `annual leave`, `sick leave`, `holiday`, `vacation`

**Custom Prompt Example:**
```
You are an expert in KFG leave policy analysis...

The response must be structured as follows:

1. **Leave Policy Response**: Provide a clear, concise title...
2. **Leave Types Available**: List all types of leave mentioned...
3. **Duration and Limits**: Detail the duration for each leave type...
4. **Approval Process**: Describe the approval procedure...
5. **Documentation Required**: Specify what documents are needed...
6. **Source Documents**: List the specific policy documents used...

Extract specific leave entitlements, approval authorities, and documentation requirements directly from the policy documents.
```

### **4. ✈️ Travel Policy Queries**
**Patterns Detected:** `travel allowance`, `ta da`, `transport`, `fuel allowance`, `car allowance`

**Custom Prompt Example:**
```
You are an expert in KFG travel and allowance policy analysis...

The response must be structured as follows:

1. **Travel Policy Response**: Provide a clear, concise title...
2. **Allowance Rates**: Detail the specific rates for different types...
3. **Limits and Conditions**: Specify any limits on travel allowances...
4. **Approval Requirements**: Describe the approval process...
5. **Documentation Needed**: List all required documents...
6. **Source Documents**: List the specific policy documents used...

Focus on extracting specific rates, limits, and approval procedures directly from the policy documents.
```

### **5. 🏠 Housing Policy Queries**
**Patterns Detected:** `house rent`, `accommodation`, `furniture allowance`, `housing benefits`

**Custom Prompt Example:**
```
You are an expert in KFG housing and accommodation policy analysis...

The response must be structured as follows:

1. **Housing Policy Response**: Provide a clear, concise title...
2. **Allowance Amounts**: Detail the specific amounts for housing-related benefits...
3. **Eligibility Criteria**: Describe who is eligible for housing benefits...
4. **Conditions and Restrictions**: Specify any conditions or limitations...
5. **Approval Process**: Detail the approval procedure...
6. **Source Documents**: List the specific policy documents used...

Extract specific amounts, eligibility criteria, and approval procedures directly from the policy documents.
```

## 🔧 **How to Use Custom Prompts**

### **Method 1: Use Existing Custom Prompts**
```python
from deepseek_llm import DeepSeekLLMService

# Initialize service
llm_service = DeepSeekLLMService()

# Process query with custom prompt (automatically selected based on query type)
response = llm_service.process_query_with_custom_prompt(
    query="What is the medical bill coverage?",
    policy_documents=relevant_docs
)
```

### **Method 2: Add Your Own Custom Query Types**
```python
# Add a new custom query type with your own prompt
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

Use only information explicitly stated in the documents.""",
    answer_template={
        "structure": "bonus_policy",
        "required_sections": ["title", "types", "eligibility", "calculation", "payment", "sources"],
        "format": "structured_list"
    }
)
```

### **Method 3: Get Custom Prompt for Specific Query Type**
```python
# Get the custom prompt being used for a query type
custom_prompt = llm_service.get_custom_prompt_for_query_type("medical")
print(f"Medical policy prompt: {custom_prompt[:200]}...")
```

### **Method 4: List All Available Query Types**
```python
# See what query types are available
query_types = llm_service.list_available_query_types()
for qt in query_types:
    print(f"• {qt}")

# Get detailed info about a specific type
medical_info = llm_service.get_query_type_info("medical")
print(f"Patterns: {medical_info['patterns']}")
print(f"Prompt length: {len(medical_info['prompt_example'])} characters")
```

## 🎯 **Key Benefits**

### **1. 🎨 EXACT Control Over Response Format**
- **Before**: Generic, inconsistent responses
- **After**: Structured, professional responses following your exact specifications

### **2. 📝 Custom Prompt Examples**
- **Before**: Hardcoded response templates
- **After**: Your own custom prompts that define exactly how responses should be structured

### **3. 🔍 Pattern-Based Query Detection**
- **Before**: Manual query classification
- **After**: Automatic detection using regex patterns you define

### **4. 🚀 Easy Customization**
- **Before**: Required code changes
- **After**: Simple method calls to add new query types and prompts

### **5. 📊 Quality Assurance**
- **Before**: Single-stage processing
- **After**: Multi-stage processing with custom prompt validation

## 🧪 **Testing the System**

### **Run the Demo:**
```bash
python demo_custom_prompts.py
```

### **Test Specific Functionality:**
```python
# Test custom prompt processing
response = llm_service.process_query_with_custom_prompt(
    query="What is the medical bill coverage?",
    policy_documents=docs
)

# Test adding custom types
llm_service.add_custom_query_type(
    query_type="custom_policy",
    patterns=[r"custom\s+pattern"],
    prompt_example="Your exact prompt instructions here..."
)

# Test query type management
types = llm_service.list_available_query_types()
info = llm_service.get_query_type_info("medical")
```

## 🏗️ **Architecture: How It Works**

### **1. Query Detection**
```
User Query → Regex Pattern Matching → Query Type Identification
```

### **2. Custom Prompt Selection**
```
Query Type → Custom Prompt Lookup → Prompt Template Selection
```

### **3. Document Processing**
```
Policy Documents → Context Preparation → Structured Document Context
```

### **4. Response Generation**
```
Custom Prompt + Document Context → DeepSeek Processing → Structured Response
```

## 🎯 **Example: Your Incident Report Style**

Just like your incident report example, you can now define **exact prompts** for each policy type:

```python
# Example: Medical Policy Prompt (Similar to your incident report)
medical_prompt = """You are an expert in writing accurate and professional medical policy reports for KFG.

Your task is to generate a report based on the context provided by the policy documents.

The report must be descriptive and structured as follows:

1. **Title of the Medical Policy**: [Policy Name] - Provide a clear, concise title using the exact words from the documents.

2. **Descriptive Summary**: Craft a detailed paragraph explaining the medical coverage in narrative form using only the document content. Include specific amounts, eligibility criteria, and procedures.

3. **Key Findings**: Summarize the main facts using only the documents. Extract key elements such as coverage limits, eligibility requirements, and required procedures. **Do not add or infer any details**.

4. **Action Taken**: Describe any actions or procedures mentioned in the documents. Highlight any specific requirements or steps, using only the actions described in the documents.

5. **Source Documents**: List the specific policy documents used to generate this response.

Ensure that no information is inferred or added that is not explicitly stated in the policy documents."""
```

## 🚀 **Next Steps**

### **1. Test the System**
```bash
python demo_custom_prompts.py
```

### **2. Customize for Your Needs**
- Modify existing prompts
- Add new query types
- Adjust response structures

### **3. Integrate with Your Chatbot**
- Replace standard responses with custom prompt responses
- Monitor quality improvements
- Iterate and refine

## 🎉 **Summary**

**🎯 You now have EXACT control over how your KFG Policy Chatbot responds!**

- **Custom Prompts**: Define exactly how each query type is answered
- **Pattern Detection**: Automatic query classification using regex
- **Structured Responses**: Professional, consistent formatting
- **Easy Customization**: Simple methods to add new query types
- **Quality Control**: Multi-stage processing with custom validation

**This is exactly what you wanted - precise control over answer formats and content, just like your incident report example!** 🚀

Instead of generic answers, you get:
- 🏥 **Medical queries** → Your exact medical policy prompt structure
- 💰 **Salary queries** → Your exact salary policy prompt structure  
- 📅 **Leave queries** → Your exact leave policy prompt structure
- ✈️ **Travel queries** → Your exact travel policy prompt structure
- 🏠 **Housing queries** → Your exact housing policy prompt structure

**🎯 Complete control over response formats and content!** 