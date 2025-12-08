import requests
import json

BASE = "http://localhost:8000/api"

print("\n" + "="*70)
print("TESTING ALL FEATURES WITH OPENAI")
print("="*70)

# Test 1: Server
print("\n1. Server Health...")
r = requests.get("http://localhost:8000/")
print(f"✅ Server: {r.json()['message']}")

# Test 2: Create User
print("\n2. Creating Test User...")
user_data = {
    "email": "aitest@test.com",
    "password": "Test123!",
    "full_name": "AI Test",
    "company": "TestCo"
}
r = requests.post(f"{BASE}/auth/signup", json=user_data)
if r.status_code in [200, 201]:
    token = r.json()['access_token']
    print(f"✅ User created, token: {token[:20]}...")
else:
    # Try login
    r = requests.post(f"{BASE}/auth/login", json={"email": "aitest@test.com", "password": "Test123!"})
    token = r.json()['access_token']
    print(f"✅ User exists, logged in: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# Test 3: AI Chatbot
print("\n3. Testing AI Chatbot...")
chat_data = {"message": "What is revenue leakage and how can I prevent it?"}
r = requests.post(f"{BASE}/chatbot", json=chat_data, headers=headers)

if r.status_code == 200:
    data = r.json()
    print(f"✅ AI Response received!")
    print(f"   Topic: {data.get('topic')}")
    print(f"   Answer length: {len(data.get('answer', ''))} characters")
    print(f"   Answer preview: {data.get('answer', '')[:200]}...")
    print(f"   Suggestions: {len(data.get('suggestions', []))}")
else:
    print(f"❌ Chatbot error: {r.status_code}")
    print(f"   Response: {r.text}")

# Test 4: Upload Sample File
print("\n4. Testing File Upload & Analysis...")
import os
sample_file = "Sample_Revenue_Data.xlsx"

if os.path.exists(sample_file):
    with open(sample_file, 'rb') as f:
        files = {'file': f}
        r = requests.post(f"{BASE}/upload/", files=files, headers=headers)
    
    if r.status_code == 200:
        result = r.json()
        print(f"✅ File uploaded successfully!")
        print(f"   Upload ID: {result.get('id')}")
        
        if 'analysis_data' in result:
            analysis = result['analysis_data']
            print(f"   Total Revenue: ${analysis.get('total_revenue', 0):,.2f}")
            print(f"   Issues Found: {len(analysis.get('leakage_items', []))}")
            
            # Show leakages
            for item in analysis.get('leakage_items', [])[:3]:
                print(f"   - {item['type']}: ${item['amount']:,.2f} ({item['severity']})")
        
        # Check AI analysis
        if result.get('ai_analysis'):
            print(f"   AI Analysis: {len(result['ai_analysis'])} characters")
            print(f"   Preview: {result['ai_analysis'][:150]}...")
        else:
            print(f"   ⚠️ No AI analysis in response")
    else:
        print(f"❌ Upload failed: {r.status_code}")
else:
    print(f"⚠️ Sample file not found")

# Test 5: Dashboard
print("\n5. Testing Dashboard...")
r = requests.get(f"{BASE}/dashboard/", headers=headers)
if r.status_code == 200:
    data = r.json()
    print(f"✅ Dashboard working!")
    print(f"   Uploads: {data.get('total_uploads')}")
    print(f"   Revenue: ${data.get('total_revenue', 0):,.2f}")

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70 + "\n")
