"""
Quick database check and update
"""
import sys
sys.path.insert(0, 'd:\\Revenu_system\\backend')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_engine('sqlite:///../revenue_advisor.db')
Session = sessionmaker(bind=engine)
db = Session()

# Import models after engine is created
from database.database import User, BusinessAnalysis

print("=" * 60)
print("          DATABASE CHECK")
print("=" * 60)

# Check users
users = db.query(User).all()
print(f"\n📊 Total Users: {len(users)}")
for user in users:
    print(f"   ID: {user.id} | Email: {user.email} | Role: {user.role}")

# Check analyses
analyses = db.query(BusinessAnalysis).all()
print(f"\n📊 Total Analyses: {len(analyses)}")

analyses_without_user = [a for a in analyses if a.user_id is None]
print(f"   Analyses without user_id: {len(analyses_without_user)}")

if analyses_without_user:
    print("\n⚠️  Found analyses without user_id. Assigning to admin...")
    admin = db.query(User).filter(User.role == 'admin').first()
    
    if admin:
        for analysis in analyses_without_user:
            analysis.user_id = admin.id
            print(f"   ✅ Assigned analysis '{analysis.business_name}' to {admin.email}")
        
        db.commit()
        print(f"\n✅ Updated {len(analyses_without_user)} analyses")
    else:
        print("❌ No admin user found")
else:
    print("✅ All analyses have user_id")

# Show final stats
print(f"\n📊 Final Stats:")
for user in users:
    count = db.query(BusinessAnalysis).filter(BusinessAnalysis.user_id == user.id).count()
    print(f"   {user.email}: {count} analyses")

db.close()
print("\n" + "=" * 60)
