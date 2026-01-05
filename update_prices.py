"""
Script to update all product prices to Nigerian Naira (₦) with minimum 5000.
Run this script to update all existing products in the database.
"""
from app import app, db
from models import Product

def update_product_prices():
    """Update all product prices to meet the requirements"""
    with app.app_context():
        products = Product.query.all()
        
        if not products:
            print("No products found in database.")
            return
        
        print(f"Found {len(products)} products. Updating prices...\n")
        
        for product in products:
            old_price = float(product.price)
            
            # Convert to Naira (assuming old price was in a different currency)
            # If old price is less than 5000, set to a reasonable amount in Naira
            # If old price seems to be already in Naira or reasonable, ensure it's at least 5000
            
            if old_price < 5000:
                # Calculate a proportional price in Naira range (5000-100000)
                # Using formula: new_price = (old_price / 100) * 5000, but ensure minimum 5000
                new_price = max(5000, old_price * 100)
            else:
                # Already reasonable, keep as is
                new_price = old_price
            
            # Ensure price is at least 5000
            if new_price < 5000:
                new_price = 5000
            
            product.price = new_price
            
            print(f"✓ {product.name}")
            print(f"  Old Price: ₦{old_price:,.2f}")
            print(f"  New Price: ₦{new_price:,.2f}")
            print()
        
        # Commit all changes
        db.session.commit()
        print(f"\n✅ Successfully updated {len(products)} products!")
        print("All prices are now in Naira (₦) with minimum ₦5,000")

if __name__ == "__main__":
    update_product_prices()
