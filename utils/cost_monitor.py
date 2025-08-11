#!/usr/bin/env python3
"""
Cost Monitor for KFG Policy Chatbot
Tracks API usage and estimates costs
"""

import json
import time
from datetime import datetime
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import Config

class CostMonitor:
    def __init__(self):
        self.usage_file = Path("api_usage.json")
        self.load_usage()
    
    def load_usage(self):
        """Load usage data from file"""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    self.usage_data = json.load(f)
            except:
                self.usage_data = self._init_usage_data()
        else:
            self.usage_data = self._init_usage_data()
    
    def _init_usage_data(self):
        """Initialize usage data structure"""
        return {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost_usd": 0.0,
            "daily_usage": {},
            "monthly_usage": {},
            "last_reset": datetime.now().isoformat()
        }
    
    def save_usage(self):
        """Save usage data to file"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage_data, f, indent=2)
    
    def record_request(self, tokens_used, cost_usd=None):
        """Record an API request"""
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        
        # Update totals
        self.usage_data["total_requests"] += 1
        self.usage_data["total_tokens"] += tokens_used
        
        # Estimate cost if not provided (DeepSeek pricing: ~$0.002 per 1K tokens)
        if cost_usd is None:
            cost_usd = (tokens_used / 1000) * 0.002
        
        self.usage_data["total_cost_usd"] += cost_usd
        
        # Update daily usage
        if today not in self.usage_data["daily_usage"]:
            self.usage_data["daily_usage"][today] = {
                "requests": 0,
                "tokens": 0,
                "cost_usd": 0.0
            }
        
        self.usage_data["daily_usage"][today]["requests"] += 1
        self.usage_data["daily_usage"][today]["tokens"] += tokens_used
        self.usage_data["daily_usage"][today]["cost_usd"] += cost_usd
        
        # Update monthly usage
        if month not in self.usage_data["monthly_usage"]:
            self.usage_data["monthly_usage"][month] = {
                "requests": 0,
                "tokens": 0,
                "cost_usd": 0.0
            }
        
        self.usage_data["monthly_usage"][month]["requests"] += 1
        self.usage_data["monthly_usage"][month]["tokens"] += tokens_used
        self.usage_data["monthly_usage"][month]["cost_usd"] += cost_usd
        
        self.save_usage()
    
    def get_usage_summary(self):
        """Get current usage summary"""
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%Y-%m")
        
        today_usage = self.usage_data["daily_usage"].get(today, {
            "requests": 0,
            "tokens": 0,
            "cost_usd": 0.0
        })
        
        month_usage = self.usage_data["monthly_usage"].get(month, {
            "requests": 0,
            "tokens": 0,
            "cost_usd": 0.0
        })
        
        return {
            "total": {
                "requests": self.usage_data["total_requests"],
                "tokens": self.usage_data["total_tokens"],
                "cost_usd": self.usage_data["total_cost_usd"]
            },
            "today": today_usage,
            "this_month": month_usage
        }
    
    def print_usage_report(self):
        """Print a formatted usage report"""
        summary = self.get_usage_summary()
        
        print("💰 API Usage Report")
        print("=" * 50)
        print(f"📊 Total Usage:")
        print(f"   Requests: {summary['total']['requests']:,}")
        print(f"   Tokens: {summary['total']['tokens']:,}")
        print(f"   Cost: ${summary['total']['cost_usd']:.4f}")
        print()
        print(f"📅 Today's Usage:")
        print(f"   Requests: {summary['today']['requests']}")
        print(f"   Tokens: {summary['today']['tokens']:,}")
        print(f"   Cost: ${summary['today']['cost_usd']:.4f}")
        print()
        print(f"📆 This Month:")
        print(f"   Requests: {summary['this_month']['requests']}")
        print(f"   Tokens: {summary['this_month']['tokens']:,}")
        print(f"   Cost: ${summary['this_month']['cost_usd']:.4f}")
        print()
        
        # Cost projections
        if summary['today']['requests'] > 0:
            avg_tokens_per_request = summary['today']['tokens'] / summary['today']['requests']
            estimated_monthly_cost = avg_tokens_per_request * 30 * 0.002 / 1000
            print(f"📈 Estimated monthly cost at current usage: ${estimated_monthly_cost:.2f}")
    
    def reset_usage(self):
        """Reset usage data"""
        self.usage_data = self._init_usage_data()
        self.save_usage()
        print("✅ Usage data reset successfully")

# Global cost monitor instance
cost_monitor = CostMonitor()

def monitor_api_call(func):
    """Decorator to monitor API calls"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Estimate tokens (rough approximation)
        # This is a simplified estimation - actual token count would come from API response
        estimated_tokens = len(str(result)) // 4  # Rough estimate: 4 chars per token
        
        cost_monitor.record_request(estimated_tokens)
        
        return result
    return wrapper

if __name__ == "__main__":
    # Print usage report
    cost_monitor.print_usage_report()
    
    # Interactive menu
    while True:
        print("\nOptions:")
        print("1. View usage report")
        print("2. Reset usage data")
        print("3. Exit")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            cost_monitor.print_usage_report()
        elif choice == "2":
            confirm = input("Are you sure you want to reset usage data? (y/N): ").strip().lower()
            if confirm == 'y':
                cost_monitor.reset_usage()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.") 