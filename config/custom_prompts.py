"""
Custom Policy Prompts Configuration
Provides specific, accurate answers for common KFG policy questions
"""

class CustomPrompts:
    """Custom prompts for specific policy questions"""
    
    # Medical Allowance Policy
    MEDICAL_ALLOWANCE = {
        "keywords": ["medical allowance", "medical bill", "medical policy", "health allowance", "medical claim"],
        "response": """**Medical Allowance Policy:**

**Job Group 1 to 3 (Non-Management):**
- Maximum: 40,000 Taka

**Job Group 4 to 12:**
- Maximum: 80,000 Taka OR Monthly Gross Salary (whichever is higher)

*This policy ensures appropriate medical coverage based on job level and salary structure.*""",
        "confidence_boost": 0.9,  # High confidence for custom prompts
        "source": "Custom Policy Knowledge Base"
    }
    
    # TA-DA Policy
    TA_DA_POLICY = {
        "keywords": ["ta da", "travel allowance", "daily allowance", "tour allowance", "travel policy"],
        "response": """**TA-DA Policy (KFL & KML):**

**Travel Allowance (TA):**
- Based on distance and mode of transport
- Varies by job group and destination

**Daily Allowance (DA):**
- Outstation work: Standard daily rates apply
- Local work: No DA applicable

*Please refer to specific TA-DA policy documents for detailed rates and conditions.*""",
        "confidence_boost": 0.85,
        "source": "Custom Policy Knowledge Base"
    }
    
    # Leave Policy
    LEAVE_POLICY = {
        "keywords": ["leave", "leave policy", "annual leave", "sick leave", "casual leave", "maternity leave"],
        "response": """**Leave Policy Overview:**

**Annual Leave:**
- Management: 30 days per year
- Non-management: 20 days per year

**Sick Leave:**
- With medical certificate: Up to 30 days
- Without certificate: Up to 7 days

**Casual Leave:**
- 10 days per year

*Specific leave entitlements may vary by job group and service length.*""",
        "confidence_boost": 0.8,
        "source": "Custom Policy Knowledge Base"
    }
    
    # Add more custom prompts here as needed
    CUSTOM_PROMPTS = {
        "medical_allowance": MEDICAL_ALLOWANCE,
        "ta_da_policy": TA_DA_POLICY,
        "leave_policy": LEAVE_POLICY
    }
    
    @classmethod
    def get_custom_response(cls, query: str) -> dict:
        """Get custom response if query matches any custom prompt keywords"""
        query_lower = query.lower()
        
        for prompt_key, prompt_data in cls.CUSTOM_PROMPTS.items():
            for keyword in prompt_data["keywords"]:
                if keyword in query_lower:
                    return {
                        "has_custom_response": True,
                        "response": prompt_data["response"],
                        "confidence": prompt_data["confidence_boost"],
                        "source": prompt_data["source"],
                        "prompt_type": prompt_key
                    }
        
        return {"has_custom_response": False}
    
    @classmethod
    def get_all_prompts(cls) -> dict:
        """Get all available custom prompts"""
        return cls.CUSTOM_PROMPTS 