"""
Create demo users for testing - Admin and User roles
"""
import hashlib
from database.database import SessionLocal, User, init_db

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_demo_users():
    """Create demo user accounts for admin and user roles"""
    init_db()
    db = SessionLocal()
    
    demo_users = [
        {
            "email": "admin@revenue.com",
            "password": "admin123",
            "full_name": "Admin User",
            "company_name": "Revenue Advisor",
            "role": "admin"
        },
        {
            "email": "user@revenue.com",
            "password": "user123",
            "full_name": "Regular User",
            "company_name": "Revenue Advisor",
            "role": "user"
        }
    ]
    
    try:
        print("\n" + "="*60)
        print("Creating Demo Users".center(60))
        print("="*60 + "\n")
        
        for user_data in demo_users:
            # Check if user exists
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            
            if existing_user:
                print(f"✅ {user_data['role']} user already exists: {user_data['email']}")
            else:
                # Create new user
                new_user = User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    company_name=user_data["company_name"],
                    role=user_data["role"]
                )
                db.add(new_user)
                db.commit()
                print(f"✅ {user_data['role']} user created: {user_data['email']}")
        
        print("\n" + "="*60)
        print("Demo Credentials".center(60))
        print("="*60 + "\n")
        
        for user_data in demo_users:
            print(f"🔐 {user_data['role'].upper()}")
            print(f"   Email:    {user_data['email']}")
            print(f"   Password: {user_data['password']}")
            print()
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error creating demo users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_users()
