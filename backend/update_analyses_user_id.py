"""
Update existing business analyses to have user_id
This script assigns existing analyses without user_id to the admin user
"""

from database.database import SessionLocal, BusinessAnalysis, User

def update_analyses_user_id():
    db = SessionLocal()
    
    try:
        # Get admin user
        admin = db.query(User).filter(User.email == "admin@revenue.com").first()
        if not admin:
            print("❌ Admin user not found. Run create_demo_user.py first.")
            return
        
        # Get all analyses without user_id
        analyses_without_user = db.query(BusinessAnalysis).filter(
            BusinessAnalysis.user_id == None
        ).all()
        
        if not analyses_without_user:
            print("✅ All analyses already have user_id assigned")
            
            # Show statistics
            total_analyses = db.query(BusinessAnalysis).count()
            admin_analyses = db.query(BusinessAnalysis).filter(
                BusinessAnalysis.user_id == admin.id
            ).count()
            
            print(f"\n📊 Analysis Statistics:")
            print(f"   Total analyses: {total_analyses}")
            print(f"   Admin's analyses: {admin_analyses}")
            
            # List all users with their analysis count
            users = db.query(User).all()
            print(f"\n👥 Users and their analyses:")
            for user in users:
                user_analyses = db.query(BusinessAnalysis).filter(
                    BusinessAnalysis.user_id == user.id
                ).count()
                print(f"   {user.email} ({user.role}): {user_analyses} analyses")
            
            return
        
        # Assign them to admin
        count = 0
        for analysis in analyses_without_user:
            analysis.user_id = admin.id
            count += 1
        
        db.commit()
        
        print(f"✅ Updated {count} analyses to be owned by {admin.email}")
        
        # Show updated statistics
        total_analyses = db.query(BusinessAnalysis).count()
        admin_analyses = db.query(BusinessAnalysis).filter(
            BusinessAnalysis.user_id == admin.id
        ).count()
        
        print(f"\n📊 Updated Analysis Statistics:")
        print(f"   Total analyses: {total_analyses}")
        print(f"   Admin's analyses: {admin_analyses}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("          Updating Business Analyses User ID")
    print("=" * 60)
    print()
    
    update_analyses_user_id()
    
    print()
    print("=" * 60)
