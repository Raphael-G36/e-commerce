"""
Chatbot service using Groq AI
"""
from dotenv import load_dotenv
import os
from groq import Groq
from models import Product, db

load_dotenv()

class ChatbotService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"
        self.product_cache = None
        self.cache_timestamp = None
        self.system_prompt = None
        self._prompt_initialized = False
    
    def _ensure_prompt_initialized(self):
        """Ensure system prompt is built (lazy initialization)"""
        if not self._prompt_initialized:
            self._build_dynamic_prompt()
            self._prompt_initialized = True
    
    def _build_dynamic_prompt(self):
        """Build system prompt with current store inventory information"""
        products = self.get_all_products()
        
        # Get store statistics
        total_products = len(products)
        categories = set()
        price_range = []
        product_catalog = []
        
        for p in products:
            categories.add(p['category'])
            price_range.append(p['price'])
            # Create detailed product listing
            stock_status = "In Stock" if p['stock'] > 0 else "Out of Stock"
            product_catalog.append(
                f"• {p['name']} - ₦{p['price']:,.2f} ({p['category']}) - {stock_status} - Stock: {p['stock']} units"
            )
        
        categories_text = ", ".join(sorted(categories)) if categories else "various categories"
        catalog_text = "\n".join(product_catalog) if product_catalog else "No products available"
        
        self.system_prompt = f"""You are a knowledgeable and friendly customer service assistant for ShopHub, a premier e-commerce store.

STORE INFORMATION:
- Total Products: {total_products}
- Categories: {categories_text}
- Price Range: ₦{min(price_range) if price_range else 0:,.2f} - ₦{max(price_range) if price_range else 0:,.2f}

COMPLETE PRODUCT CATALOG (ONLY THESE PRODUCTS ARE AVAILABLE):
{catalog_text}

Your responsibilities:
1. Provide accurate product information ONLY from our catalog above
2. Make personalized product recommendations based on ACTUAL inventory
3. Answer questions about pricing, availability, and stock
4. Assist with order inquiries and tracking
5. Explain shipping and return policies
6. Provide excellent customer service

Store Policies:
- Free shipping on orders over ₦25,000
- 30-day money-back return policy
- Secure payment processing
- 24/7 customer support available

⚠️ CRITICAL INSTRUCTIONS:
- ONLY RECOMMEND PRODUCTS FROM THE CATALOG ABOVE - DO NOT INVENT OR SUGGEST PRODUCTS NOT LISTED
- When customers ask about products, REFER EXCLUSIVELY to our actual inventory
- Provide SPECIFIC product names, exact prices (in Nigerian Naira ₦), and ACTUAL availability
- All prices are in Nigerian Naira (₦)
- If a product isn't in stock or not in our catalog, suggest SIMILAR IN-STOCK alternatives from the catalog
- Be HONEST about what we have in stock
- For product recommendations, consider customer preferences and available budget
- Always mention ACTUAL stock availability
- NEVER make up product names or features
- If unsure about a product detail, admit it rather than guess

Tone: Be friendly, professional, helpful, and conversational. Keep responses concise but informative."""
    
    def get_all_products(self):
        """Get all products from database"""
        try:
            products = Product.query.all()
            product_list = []
            for p in products:
                product_list.append({
                    'id': p.id,
                    'name': p.name,
                    'price': float(p.price),
                    'category': p.category,
                    'stock': p.stock,
                    'description': p.description,
                    'featured': p.featured
                })
            return product_list
        except Exception as e:
            print(f"Error fetching all products: {e}")
            return []
    
    def get_product_info(self, query):
        """Search products based on user query"""
        try:
            # Simple keyword search
            products = Product.query.filter(
                db.or_(
                    Product.name.ilike(f'%{query}%'),
                    Product.description.ilike(f'%{query}%'),
                    Product.category.ilike(f'%{query}%')
                )
            ).limit(5).all()
            
            if products:
                product_list = []
                for p in products:
                    product_list.append({
                        'name': p.name,
                        'price': float(p.price),
                        'category': p.category,
                        'stock': p.stock,
                        'id': p.id,
                        'description': p.description
                    })
                return product_list
            return []
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_products_by_category(self, category):
        """Get products in a specific category"""
        try:
            products = Product.query.filter(
                Product.category.ilike(f'%{category}%'),
                Product.stock > 0
            ).all()
            
            product_list = []
            for p in products:
                product_list.append({
                    'name': p.name,
                    'price': float(p.price),
                    'category': p.category,
                    'stock': p.stock,
                    'id': p.id
                })
            return product_list
        except Exception as e:
            print(f"Error fetching products by category: {e}")
            return []
    
    def get_featured_products(self):
        """Get featured/recommended products"""
        try:
            products = Product.query.filter(
                Product.featured == True,
                Product.stock > 0
            ).limit(5).all()
            
            product_list = []
            for p in products:
                product_list.append({
                    'name': p.name,
                    'price': float(p.price),
                    'category': p.category,
                    'stock': p.stock,
                    'id': p.id
                })
            return product_list
        except Exception as e:
            print(f"Error fetching featured products: {e}")
            return []
    
    def format_product_info(self, products):
        """Format product information for the AI model"""
        if not products:
            return ""
        
        product_info = "\n📦 AVAILABLE PRODUCTS:\n" + "-" * 50 + "\n"
        for p in products:
            stock_status = "✅ In Stock" if p['stock'] > 0 else "❌ Out of Stock"
            product_info += f"• {p['name']}\n"
            product_info += f"  Price: ₦{p['price']:,.2f}\n"
            product_info += f"  Category: {p['category']}\n"
            product_info += f"  Status: {stock_status} ({p['stock']} units)\n"
            if 'description' in p and p['description']:
                product_info += f"  Description: {p['description'][:100]}...\n"
            product_info += "\n"
        
        return product_info
    
    def generate_response(self, user_message, conversation_history=None):
        """Generate chatbot response"""
        try:
            # Ensure prompt is initialized with app context
            self._ensure_prompt_initialized()
            
            # Check if user is asking about products
            product_keywords = ['product', 'item', 'buy', 'purchase', 'price', 'available', 'stock', 'category', 'recommend', 'what', 'have', 'show', 'find', 'look', 'suggest', 'help', 'need', 'want', 'like']
            is_product_query = any(keyword in user_message.lower() for keyword in product_keywords)
            
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Keep last 5 messages for context
            
            # Build user message with product context
            user_context = user_message
            
            # For product queries, search and add relevant product info
            if is_product_query:
                # Try specific search based on user message
                products = self.get_product_info(user_message)
                
                # If no specific matches, get featured products as suggestions
                if not products:
                    products = self.get_featured_products()
                
                # If still no products, get a broader selection
                if not products:
                    products = self.get_all_products()[:8]  # Get up to 8 products
                
                if products:
                    product_info = self.format_product_info(products)
                    user_context += product_info
                    user_context += "\n\nREMINDER: Only recommend products from the list above. Do not suggest any products not listed."
            
            messages.append({"role": "user", "content": user_context})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,  # Lower temperature for more consistent, factual responses
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later or contact our support team."


# Singleton instance
chatbot_service = ChatbotService()


