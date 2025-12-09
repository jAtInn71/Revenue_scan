"""
Database Migration Script
Adds user_id column to business_analyses and uploaded_data tables
Updates user roles to admin/user
"""
import sqlite3
import sys

DB_PATH = '../revenue_advisor.db'

def migrate_database():
    print("=" * 60)
    print("          DATABASE MIGRATION")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Step 1: Check and add user_id to business_analyses
        print("\n1️⃣  Checking business_analyses table...")
        cursor.execute("PRAGMA table_info(business_analyses)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("   Adding user_id column to business_analyses...")
            cursor.execute("ALTER TABLE business_analyses ADD COLUMN user_id INTEGER")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_business_analyses_user_id ON business_analyses(user_id)")
            print("   ✅ Added user_id column and index")
        else:
            print("   ✅ user_id column already exists")
        
        # Step 2: Check and add user_id to uploaded_data
        print("\n2️⃣  Checking uploaded_data table...")
        cursor.execute("PRAGMA table_info(uploaded_data)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("   Adding user_id column to uploaded_data...")
            cursor.execute("ALTER TABLE uploaded_data ADD COLUMN user_id INTEGER")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_uploaded_data_user_id ON uploaded_data(user_id)")
            print("   ✅ Added user_id column and index")
        else:
            print("   ✅ user_id column already exists")
        
        # Step 3: Update user roles
        print("\n3️⃣  Updating user roles...")
        cursor.execute("SELECT id, email, role FROM users")
        users = cursor.fetchall()
        
        for user_id, email, role in users:
            new_role = None
            if role is None or role == '':
                if 'admin' in email.lower():
                    new_role = 'admin'
                else:
                    new_role = 'user'
            elif role not in ['admin', 'user']:
                # Convert old roles to user
                new_role = 'user'
            
            if new_role:
                cursor.execute("UPDATE users SET role = ? WHERE id = ?", (new_role, user_id))
                print(f"   Updated {email}: {role} → {new_role}")
        
        # Step 4: Assign existing analyses to first admin user
        print("\n4️⃣  Assigning analyses to users...")
        cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
        admin_result = cursor.fetchone()
        
        if admin_result:
            admin_id = admin_result[0]
            cursor.execute("SELECT COUNT(*) FROM business_analyses WHERE user_id IS NULL")
            unassigned_count = cursor.fetchone()[0]
            
            if unassigned_count > 0:
                cursor.execute("UPDATE business_analyses SET user_id = ? WHERE user_id IS NULL", (admin_id,))
                print(f"   ✅ Assigned {unassigned_count} analyses to admin")
            else:
                print("   ✅ All analyses already assigned")
        else:
            print("   ⚠️  No admin user found, skipping analysis assignment")
        
        # Step 5: Assign existing uploads to first admin user
        print("\n5️⃣  Assigning uploads to users...")
        if admin_result:
            cursor.execute("SELECT COUNT(*) FROM uploaded_data WHERE user_id IS NULL")
            unassigned_count = cursor.fetchone()[0]
            
            if unassigned_count > 0:
                cursor.execute("UPDATE uploaded_data SET user_id = ? WHERE user_id IS NULL", (admin_id,))
                print(f"   ✅ Assigned {unassigned_count} uploads to admin")
            else:
                print("   ✅ All uploads already assigned")
        
        conn.commit()
        
        # Show final statistics
        print("\n📊 Final Statistics:")
        cursor.execute("SELECT COUNT(*) FROM users")
        print(f"   Total users: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        for role, count in cursor.fetchall():
            print(f"     - {role}: {count}")
        
        cursor.execute("SELECT COUNT(*) FROM business_analyses")
        print(f"   Total analyses: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM business_analyses WHERE user_id IS NOT NULL")
        print(f"     - Assigned: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM uploaded_data")
        print(f"   Total uploads: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM uploaded_data WHERE user_id IS NOT NULL")
        print(f"     - Assigned: {cursor.fetchone()[0]}")
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
    
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1)
