import requests
import json

BASE = "http://localhost:8000/api"

print("\n=== CHATBOT TEST ===\n")

# 1. Login
print("1. Logging in as admin...")
r = requests.post(f"{BASE}/auth/login", json={"email": "admin@revenue.com", "password": "admin123"})
if r.status_code == 200:
    token = r.json()['access_token']
    print(f"✅ Logged in successfully")
    headers = {"Authorization": f"Bearer {token}"}
else:
    print(f"❌ Login failed: {r.status_code}")
    print(r.text)
    exit(1)

# 2. Test chatbot
print("\n2. Testing chatbot...")
chat_data = {"message": "What is revenue leakage?"}
r = requests.post(f"{BASE}/chatbot", json=chat_data, headers=headers)

print(f"Status: {r.status_code}")
print(f"Response: {r.text[:500]}...")

if r.status_code == 200:
    data = r.json()
    print(f"\n✅ CHATBOT WORKING!")
    print(f"Topic: {data.get('topic')}")
    print(f"Answer: {data.get('answer', '')[:200]}...")
else:
    print(f"\n❌ CHATBOT ERROR")
    print(f"Details: {r.text}")
