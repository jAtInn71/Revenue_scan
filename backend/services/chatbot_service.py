"""
AI Business Consultant Chatbot Service
Provides intelligent business advice, revenue optimization, and strategic guidance
"""

from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from datetime import datetime
from core.config import settings


class BusinessChatbot:
    """
    Intelligent AI chatbot for business questions and revenue optimization advice
    """
    
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "":
            try:
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.client = None
        
        # Business knowledge base topics
        self.topics = {
            "revenue": ["increase sales", "boost revenue", "grow income", "maximize profit"],
            "costs": ["reduce costs", "cut expenses", "save money", "optimize spending"],
            "pricing": ["pricing strategy", "price optimization", "discount policy", "value pricing"],
            "customers": ["customer retention", "acquisition", "lifetime value", "churn"],
            "marketing": ["marketing strategy", "advertising", "promotion", "branding"],
            "operations": ["efficiency", "automation", "workflow", "productivity"],
            "finance": ["cash flow", "profitability", "margins", "financial health"],
            "strategy": ["business strategy", "growth plan", "expansion", "scale"],
            "data": ["analytics", "reporting", "metrics", "kpis"],
            "leakage": ["revenue leakage", "loss prevention", "fraud detection", "waste"]
        }
    
    async def chat(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and return intelligent business advice
        
        Args:
            message: User's question or message
            context: Optional context (user data, recent analyses, etc.)
            conversation_history: Previous messages in conversation
        
        Returns:
            Response with answer, suggestions, and resources
        """
        
        if not self.client:
            return self._fallback_response(message, context)
        
        try:
            # Build context for AI
            context_str = self._build_context(context)
            
            # Prepare conversation messages
            messages = [
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                }
            ]
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Last 10 messages
            
            # Add context if available
            if context_str:
                messages.append({
                    "role": "system",
                    "content": f"CURRENT USER CONTEXT:\n{context_str}"
                })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Get AI response
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            # Identify topic and provide related suggestions
            topic = self._identify_topic(message)
            suggestions = self._get_suggestions(topic)
            resources = self._get_resources(topic)
            
            return {
                "answer": answer,
                "topic": topic,
                "suggestions": suggestions,
                "resources": resources,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return self._fallback_response(message, context)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI chatbot"""
        return """You are an expert business consultant and revenue optimization advisor with 25+ years of experience. 
You specialize in:
- Revenue growth and profit optimization
- Cost reduction and efficiency improvement
- Pricing strategies and discount management
- Customer acquisition and retention
- Financial analysis and business metrics
- Operational excellence
- Data-driven decision making
- Revenue leakage prevention

Your responses should be:
✅ ACTIONABLE - Provide specific steps, not generic advice
✅ DATA-DRIVEN - Use numbers, metrics, and benchmarks
✅ PRACTICAL - Focus on implementable solutions
✅ CONCISE - Be clear and to the point (200-400 words)
✅ STRUCTURED - Use bullet points and sections
✅ REALISTIC - Consider business constraints and resources
✅ STRATEGIC - Think long-term, not just quick fixes

When answering:
1. Start with a direct answer (1-2 sentences)
2. Provide 3-5 specific actionable steps
3. Include expected outcomes/metrics
4. Mention potential challenges
5. Suggest next steps or resources

Use a professional but friendly tone. Be encouraging and supportive."""
    
    def _build_context(self, context: Optional[Dict[str, Any]]) -> str:
        """Build context string from user data"""
        if not context:
            return ""
        
        context_parts = []
        
        # User info
        if "user" in context:
            user = context["user"]
            context_parts.append(f"User: {user.get('email', 'Unknown')}")
            if user.get('company'):
                context_parts.append(f"Company: {user['company']}")
        
        # Recent analyses
        if "recent_analyses" in context and context["recent_analyses"]:
            analyses = context["recent_analyses"]
            total_revenue = sum(a.get("total_revenue", 0) for a in analyses)
            total_leakage = sum(a.get("leakage_amount", 0) for a in analyses)
            
            context_parts.append(f"\nRecent Analysis Summary:")
            context_parts.append(f"- Total Revenue Analyzed: ${total_revenue:,.2f}")
            context_parts.append(f"- Revenue Leakage Detected: ${total_leakage:,.2f}")
            context_parts.append(f"- Number of Analyses: {len(analyses)}")
        
        # Latest upload
        if "latest_upload" in context:
            upload = context["latest_upload"]
            context_parts.append(f"\nLatest Upload:")
            context_parts.append(f"- File: {upload.get('file_name', 'N/A')}")
            context_parts.append(f"- Rows: {upload.get('total_rows', 0):,}")
            context_parts.append(f"- Issues Found: {upload.get('leakages_detected', 0)}")
        
        return "\n".join(context_parts)
    
    def _identify_topic(self, message: str) -> str:
        """Identify the main topic of the message"""
        message_lower = message.lower()
        
        for topic, keywords in self.topics.items():
            if any(keyword in message_lower for keyword in keywords):
                return topic
        
        return "general"
    
    def _get_suggestions(self, topic: str) -> List[str]:
        """Get follow-up suggestions based on topic"""
        suggestions_map = {
            "revenue": [
                "How can I increase my average transaction value?",
                "What pricing strategies work best for my industry?",
                "How do I identify underpriced products?",
                "What are quick wins to boost sales?"
            ],
            "costs": [
                "Where should I look for cost savings first?",
                "How can I reduce operational expenses?",
                "What costs typically have the highest ROI when reduced?",
                "How do I negotiate better supplier contracts?"
            ],
            "pricing": [
                "How do I set optimal prices for my products?",
                "When should I offer discounts?",
                "How can I implement value-based pricing?",
                "What's a healthy discount percentage?"
            ],
            "customers": [
                "How do I improve customer retention?",
                "What's the best way to calculate customer lifetime value?",
                "How can I reduce customer churn?",
                "What metrics should I track for customer health?"
            ],
            "leakage": [
                "What are the most common types of revenue leakage?",
                "How can I prevent revenue loss?",
                "What systems help detect leakage?",
                "How do I audit for revenue leaks?"
            ],
            "general": [
                "How can I improve my business profitability?",
                "What metrics should I track daily?",
                "How do I analyze my revenue data?",
                "What are common business financial mistakes?"
            ]
        }
        
        return suggestions_map.get(topic, suggestions_map["general"])
    
    def _get_resources(self, topic: str) -> List[Dict[str, str]]:
        """Get relevant resources based on topic"""
        resources_map = {
            "revenue": [
                {"title": "Upload Revenue Data", "action": "upload", "description": "Analyze your transactions for revenue opportunities"},
                {"title": "View Dashboard", "action": "dashboard", "description": "See your revenue metrics and trends"},
                {"title": "Generate Report", "action": "reports", "description": "Create comprehensive revenue analysis report"}
            ],
            "costs": [
                {"title": "Cost Analysis", "action": "upload", "description": "Upload expense data for cost optimization"},
                {"title": "Profitability Report", "action": "reports", "description": "Analyze profit margins and cost structure"}
            ],
            "pricing": [
                {"title": "Price Analysis", "action": "upload", "description": "Upload pricing data to detect inconsistencies"},
                {"title": "Discount Report", "action": "reports", "description": "Review discount patterns and effectiveness"}
            ],
            "leakage": [
                {"title": "Leakage Detection", "action": "upload", "description": "Upload data to identify revenue leaks"},
                {"title": "Set Up Alerts", "action": "alerts", "description": "Configure automatic leakage alerts"},
                {"title": "View Findings", "action": "dashboard", "description": "Review detected leakage points"}
            ]
        }
        
        return resources_map.get(topic, resources_map.get("revenue", []))
    
    def _fallback_response(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Provide fallback response when AI is unavailable"""
        
        topic = self._identify_topic(message)
        
        fallback_answers = {
            "revenue": "To increase revenue, focus on: 1) Analyzing pricing strategy for optimization opportunities, 2) Identifying and eliminating revenue leakage, 3) Improving average transaction value through upselling and cross-selling, 4) Enhancing customer retention to boost lifetime value. Upload your revenue data for a detailed analysis with specific recommendations.",
            
            "costs": "Cost reduction strategies: 1) Audit all expenses and categorize by necessity vs. optional, 2) Negotiate better terms with suppliers, 3) Automate manual processes to save labor costs, 4) Eliminate underperforming products/services that drain resources. Upload your expense data to identify specific savings opportunities.",
            
            "pricing": "Effective pricing strategies: 1) Research competitor pricing, 2) Calculate your true costs including overhead, 3) Set prices to achieve 25-30% profit margin minimum, 4) Limit discounts to 10-15% maximum, 5) Use tiered pricing for different customer segments. Upload your transaction data to detect pricing inconsistencies.",
            
            "leakage": "Common revenue leakages include: 1) Excessive discounts (>15% of revenue), 2) Billing errors and uncollected payments, 3) Inventory shrinkage and theft, 4) Pricing inconsistencies across channels, 5) Unrecorded sales. Upload your financial data to detect and quantify leakages in your business.",
            
            "customers": "Customer retention strategies: 1) Track customer satisfaction regularly, 2) Implement loyalty programs, 3) Provide excellent customer service, 4) Offer personalized experiences, 5) Collect and act on feedback. Calculate your customer lifetime value to prioritize retention efforts.",
            
            "general": "For business improvement, focus on: 1) Analyzing your financial data regularly, 2) Tracking key metrics (revenue, profit margin, customer acquisition cost), 3) Identifying and fixing revenue leakage, 4) Optimizing pricing strategy, 5) Improving operational efficiency. Upload your business data for personalized insights."
        }
        
        answer = fallback_answers.get(topic, fallback_answers["general"])
        
        return {
            "answer": answer,
            "topic": topic,
            "suggestions": self._get_suggestions(topic),
            "resources": self._get_resources(topic),
            "timestamp": datetime.now().isoformat(),
            "mode": "fallback"
        }


# Conversation manager for maintaining chat history
class ConversationManager:
    """Manages conversation history for chatbot sessions"""
    
    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
    
    def add_message(self, user_id: str, role: str, content: str):
        """Add a message to conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "role": role,
            "content": content
        })
        
        # Keep only last 20 messages
        if len(self.conversations[user_id]) > 20:
            self.conversations[user_id] = self.conversations[user_id][-20:]
    
    def get_history(self, user_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a user"""
        return self.conversations.get(user_id, [])
    
    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
