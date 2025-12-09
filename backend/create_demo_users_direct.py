"""
Create demo users directly in the database
"""
import sqlite3
import hashlib

DB_PATH = '../revenue_advisor.db'

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_demo_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("          CREATING DEMO USERS")
    print("=" * 60)
    
    demo_users = [
        ("admin@revenue.com", "admin123", "Admin User", "Revenue Advisor", "admin"),
        ("user@revenue.com", "user123", "Regular User", "Revenue Advisor", "user")
    ]
    
    for email, password, full_name, company, role in demo_users:
        # Check if user exists
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()
        
        if existing:
            # Update role if needed
            cursor.execute("UPDATE users SET role = ? WHERE email = ?", (role, email))
            print(f"✅ Updated existing user: {email} → role: {role}")
        else:
            # Create new user
            hashed_password = get_password_hash(password)
            cursor.execute("""
                INSERT INTO users (email, hashed_password, full_name, company_name, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, 1, datetime('now'))
            """, (email, hashed_password, full_name, company, role))
            print(f"✅ Created new user: {email} → role: {role}")
    
    conn.commit()
    
    # Show all users
    print(f"\n📊 All Users:")
    cursor.execute("SELECT id, email, role, is_active FROM users")
    for user_id, email, role, is_active in cursor.fetchall():
        status = "Active" if is_active else "Inactive"
        print(f"   {email} → {role} ({status})")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("DEMO CREDENTIALS:")
    print("=" * 60)
    print("🔐 ADMIN")
    print("   Email:    admin@revenue.com")
    print("   Password: admin123")
    print()
    print("🔐 USER")
    print("   Email:    user@revenue.com")
    print("   Password: user123")
    print("=" * 60)

if __name__ == "__main__":
    create_demo_users()
