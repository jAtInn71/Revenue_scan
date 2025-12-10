"""
Fix NULL roles in the database
"""
import sys
sys.path.insert(0, '.')

from database.database import SessionLocal, User

def fix_null_roles():
    """Update all users with NULL roles to 'user'"""
    db = SessionLocal()
    try:
        # Find users with NULL roles
        users_with_null_roles = db.query(User).filter(User.role == None).all()
        
        if not users_with_null_roles:
            print("✅ No users with NULL roles found")
            return
        
        print(f"Found {len(users_with_null_roles)} users with NULL roles")
        
        # Update each user
        for user in users_with_null_roles:
            user.role = "user"
            print(f"  - Updated user: {user.email} -> role: 'user'")
        
        db.commit()
        print(f"\n✅ Successfully updated {len(users_with_null_roles)} users")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_null_roles()
