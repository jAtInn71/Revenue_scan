import requests
import json

# Base URL
BASE_URL = "http://localhost:8000/api"

print("🧪 Testing Backend API Endpoints\n")
print("=" * 60)

# Test 1: Health Check
print("\n1️⃣ Testing Server Health...")
try:
    response = requests.get(f"{BASE_URL.replace('/api', '')}/")
    print(f"✅ Server is running: {response.json()}")
except Exception as e:
    print(f"❌ Server check failed: {e}")

# Test 2: Chatbot Topics
print("\n2️⃣ Testing Chatbot Topics Endpoint...")
try:
    response = requests.get(f"{BASE_URL}/chatbot/topics")
    data = response.json()
    print(f"✅ Topics loaded: {len(data.get('topics', {}))} categories")
    topics_list = list(data.get('topics', {}).items())
    for key, topic in topics_list[:3]:
        print(f"   - {topic.get('name', key)}")
except Exception as e:
    print(f"❌ Topics test failed: {e}")

# Test 3: Chatbot Suggestions
print("\n3️⃣ Testing Chatbot Suggestions Endpoint...")
headers = {}
try:
    # Need to create a test user first
    signup_data = {
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "company": "Test Company"
    }
    
    # Try to signup (might fail if user exists, that's OK)
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        if signup_response.status_code == 200:
            print("   ✅ Test user created")
    except:
        pass
    
    # Login to get token
    login_data = {
        "username": "test@example.com",
        "password": "test123"
    }
    login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get suggestions
        response = requests.get(f"{BASE_URL}/chatbot/suggestions", headers=headers)
        data = response.json()
        print(f"✅ Suggestions loaded: {len(data.get('suggestions', []))} suggestions")
        for sug in data.get('suggestions', [])[:3]:
            print(f"   - {sug['question']}")
    else:
        print(f"⚠️  Login failed, skipping authenticated tests")
        
except Exception as e:
    print(f"❌ Suggestions test failed: {e}")

# Test 4: Chatbot Chat
print("\n4️⃣ Testing Chatbot Chat Endpoint...")
try:
    # Use the token from previous test
    chat_data = {
        "message": "What is revenue leakage?"
    }
    
    response = requests.post(f"{BASE_URL}/chatbot", json=chat_data, headers=headers)
    data = response.json()
    
    if response.status_code == 200:
        print(f"✅ Chat response received")
        print(f"   Topic: {data.get('topic', 'N/A')}")
        print(f"   Answer length: {len(data.get('answer', ''))} characters")
        print(f"   Suggestions: {len(data.get('suggestions', []))} follow-ups")
    else:
        print(f"❌ Chat failed: {data}")
        
except Exception as e:
    print(f"❌ Chat test failed: {e}")

# Test 5: Enhanced Leakage Analyzer (via Upload)
print("\n5️⃣ Testing Enhanced Leakage Analyzer...")
try:
    # Check if sample data file exists
    import os
    sample_file = "Sample_Revenue_Data.xlsx"
    
    if os.path.exists(sample_file):
        print(f"   📁 Found sample file: {sample_file}")
        
        with open(sample_file, 'rb') as f:
            files = {'file': f}
            upload_response = requests.post(
                f"{BASE_URL}/upload/",
                files=files,
                headers=headers
            )
        
        if upload_response.status_code == 200:
            result = upload_response.json()
            print(f"✅ File uploaded and analyzed successfully")
            print(f"   Upload ID: {result.get('id', 'N/A')}")
            
            # Check analysis data
            if 'analysis_data' in result:
                analysis = result['analysis_data']
                print(f"   Total Revenue: ${analysis.get('total_revenue', 0):,.2f}")
                print(f"   Issues Found: {len(analysis.get('leakage_items', []))}")
                
                # Show top issues
                for item in analysis.get('leakage_items', [])[:3]:
                    print(f"   - {item['type']}: ${item['amount']:,.2f} ({item['severity']})")
        else:
            print(f"❌ Upload failed: {upload_response.json()}")
    else:
        print(f"⚠️  Sample file not found, skipping upload test")
        
except Exception as e:
    print(f"❌ Upload test failed: {e}")

print("\n" + "=" * 60)
print("🎉 Backend API Testing Complete!\n")
