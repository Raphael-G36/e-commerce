"""
Database initialization script.
Run this script to create the database and seed it with initial products.
"""
from app import app, db, seed_database

if __name__ == "__main__":
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        print("\nSeeding database with initial products...")
        seed_database()
        print("\nDatabase initialization complete!")


