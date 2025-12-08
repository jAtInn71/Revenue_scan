"""
COMPREHENSIVE FEATURE TEST - All Features with OpenAI Integration
"""
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_result(test_name, success, details=""):
    icon = "✅" if success else "❌"
    print(f"{icon} {test_name}")
    if details:
        print(f"   {details}")

# Initialize test results
results = {
    "passed": 0,
    "failed": 0,
    "tests": []
}

def record_test(name, passed, details=""):
    results["tests"].append({"name": name, "passed": passed, "details": details})
    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1
    print_result(name, passed, details)

print_section("🚀 COMPREHENSIVE BACKEND TESTING - ALL FEATURES")

# ============================================================================
# TEST 1: Server Health
# ============================================================================
print_section("1. SERVER HEALTH CHECK")
try:
    r = requests.get(f"{BASE_URL.replace('/api', '')}/")
    if r.status_code == 200:
        data = r.json()
        record_test("Server Status", True, f"Version: {data.get('version')}")
    else:
        record_test("Server Status", False, f"Status code: {r.status_code}")
except Exception as e:
    record_test("Server Status", False, str(e))

# ============================================================================
# TEST 2: Authentication System
# ============================================================================
print_section("2. AUTHENTICATION SYSTEM")

# Create unique test user
test_email = f"fulltest_{datetime.now().strftime('%Y%m%d%H%M%S')}@test.com"
test_password = "SecurePass123!"

try:
    # Signup
    signup_data = {
        "email": test_email,
        "password": test_password,
        "full_name": "Full Test User",
        "company": "Test Corp"
    }
    signup_r = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    if signup_r.status_code in [200, 201]:
        token = signup_r.json().get('access_token')
        record_test("User Signup", True, f"Email: {test_email}")
        record_test("JWT Token Generation", True, f"Token: {token[:20]}...")
    else:
        record_test("User Signup", False, signup_r.json())
        token = None
except Exception as e:
    record_test("User Signup", False, str(e))
    token = None

if not token:
    print("\n❌ CRITICAL: Authentication failed. Cannot proceed with authenticated tests.")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# ============================================================================
# TEST 3: File Upload & Enhanced Leakage Analysis
# ============================================================================
print_section("3. FILE UPLOAD & LEAKAGE ANALYSIS")

# Check for sample file
sample_files = [
    "Sample_Revenue_Data.xlsx",
    "../Sample_Revenue_Data.xlsx",
    "Problem_Dataset.xlsx"
]

sample_file = None
for f in sample_files:
    if os.path.exists(f):
        sample_file = f
        break

if sample_file:
    try:
        print(f"\n📁 Using sample file: {sample_file}")
        
        with open(sample_file, 'rb') as f:
            files = {'file': f}
            upload_r = requests.post(
                f"{BASE_URL}/upload/",
                files=files,
                headers=headers
            )
        
        if upload_r.status_code == 200:
            result = upload_r.json()
            upload_id = result.get('id')
            
            record_test("File Upload", True, f"Upload ID: {upload_id}")
            
            # Check analysis data
            if 'analysis_data' in result:
                analysis = result['analysis_data']
                
                # Test Enhanced Analyzer Results
                total_revenue = analysis.get('total_revenue', 0)
                record_test("Total Revenue Calculation", total_revenue > 0, 
                           f"${total_revenue:,.2f}")
                
                leakage_items = analysis.get('leakage_items', [])
                record_test("Leakage Detection", len(leakage_items) > 0, 
                           f"{len(leakage_items)} issues found")
                
                # Show top 3 leakages
                print("\n   📊 Top Leakage Issues Detected:")
                for i, item in enumerate(leakage_items[:3], 1):
                    print(f"      {i}. {item['type']}: ${item['amount']:,.2f} ({item['severity']})")
                    print(f"         → {item['description'][:80]}...")
                
                # Test specific detection algorithms
                leakage_types = [item['type'] for item in leakage_items]
                
                detection_tests = [
                    ("Negative Revenue Detection", "Negative Revenue"),
                    ("Excessive Discount Detection", "Excessive Discounts"),
                    ("Missing Data Detection", "Missing Data"),
                    ("Duplicate Detection", "Duplicate Transactions"),
                    ("Pricing Inconsistency Detection", "Pricing Inconsistencies")
                ]
                
                print("\n   🔍 Detection Algorithm Tests:")
                for test_name, leakage_type in detection_tests:
                    detected = leakage_type in leakage_types
                    if detected:
                        count = sum(1 for item in leakage_items if item['type'] == leakage_type)
                        record_test(test_name, True, f"Found {count} instances")
                    else:
                        print(f"   ℹ️  {test_name}: No issues (Good!)")
                
                # Test AI Analysis
                if 'ai_analysis' in result and result['ai_analysis']:
                    ai_text = result['ai_analysis']
                    record_test("AI Analysis Generation", len(ai_text) > 100,
                               f"{len(ai_text)} characters")
                    
                    print(f"\n   🤖 AI Analysis Preview:")
                    print(f"      {ai_text[:300]}...")
                else:
                    record_test("AI Analysis Generation", False, "No AI analysis found")
            else:
                record_test("Analysis Data Structure", False, "No analysis data")
        else:
            record_test("File Upload", False, upload_r.json())
    except Exception as e:
        record_test("File Upload & Analysis", False, str(e))
else:
    print("\n⚠️  No sample file found. Skipping upload tests.")
    print("   Run 'python create_sample_data.py' to create test files.")

# ============================================================================
# TEST 4: Chatbot Features (AI-Powered)
# ============================================================================
print_section("4. AI CHATBOT FEATURES")

# Test 4.1: Topics Endpoint
try:
    r = requests.get(f"{BASE_URL}/chatbot/topics")
    if r.status_code == 200:
        topics = r.json().get('topics', {})
        record_test("Chatbot Topics Endpoint", True, f"{len(topics)} categories")
    else:
        record_test("Chatbot Topics Endpoint", False, r.json())
except Exception as e:
    record_test("Chatbot Topics Endpoint", False, str(e))

# Test 4.2: Suggestions Endpoint
try:
    r = requests.get(f"{BASE_URL}/chatbot/suggestions", headers=headers)
    if r.status_code == 200:
        suggestions = r.json().get('suggestions', [])
        record_test("Contextual Suggestions", True, f"{len(suggestions)} suggestions")
        
        if suggestions:
            print("\n   💡 Sample Suggestions:")
            for sug in suggestions[:3]:
                q = sug.get('question', sug) if isinstance(sug, dict) else sug
                print(f"      - {q}")
    else:
        record_test("Contextual Suggestions", False, r.json())
except Exception as e:
    record_test("Contextual Suggestions", False, str(e))

# Test 4.3: Chat Functionality (Real AI Responses)
print("\n   🤖 Testing AI Chat Responses:")

test_questions = [
    ("Basic Question", "What is revenue leakage?"),
    ("Business Strategy", "How can I improve my profit margins?"),
    ("Data Analysis", "What metrics should I track for revenue optimization?")
]

for test_name, question in test_questions:
    try:
        chat_data = {"message": question}
        r = requests.post(f"{BASE_URL}/chatbot", json=chat_data, headers=headers)
        
        if r.status_code == 200:
            data = r.json()
            answer = data.get('answer', '')
            topic = data.get('topic', 'N/A')
            suggestions = data.get('suggestions', [])
            
            # Validate response quality
            has_answer = len(answer) > 50
            has_topic = topic != 'N/A'
            has_suggestions = len(suggestions) > 0
            
            all_good = has_answer and has_topic
            
            record_test(f"Chat: {test_name}", all_good,
                       f"Topic: {topic}, Answer: {len(answer)} chars, Suggestions: {len(suggestions)}")
            
            if all_good:
                print(f"      Q: {question}")
                print(f"      A: {answer[:150]}...")
                if suggestions:
                    print(f"      Follow-up: {suggestions[0] if suggestions else 'None'}")
        else:
            record_test(f"Chat: {test_name}", False, f"Status {r.status_code}")
    except Exception as e:
        record_test(f"Chat: {test_name}", False, str(e))

# ============================================================================
# TEST 5: Dashboard & Analytics
# ============================================================================
print_section("5. DASHBOARD & ANALYTICS")

try:
    r = requests.get(f"{BASE_URL}/dashboard/", headers=headers)
    if r.status_code == 200:
        data = r.json()
        record_test("Dashboard Data Retrieval", True,
                   f"Uploads: {data.get('total_uploads', 0)}, Revenue: ${data.get('total_revenue', 0):,.2f}")
        
        print(f"\n   📊 Dashboard Metrics:")
        print(f"      Total Uploads: {data.get('total_uploads', 0)}")
        print(f"      Total Revenue: ${data.get('total_revenue', 0):,.2f}")
        print(f"      Leakages Detected: {data.get('leakages_detected', 0)}")
        print(f"      Total Savings: ${data.get('total_leakage_amount', 0):,.2f}")
    else:
        record_test("Dashboard Data Retrieval", False, r.json())
except Exception as e:
    record_test("Dashboard Data Retrieval", False, str(e))

# ============================================================================
# TEST 6: Upload History
# ============================================================================
print_section("6. UPLOAD HISTORY")

try:
    r = requests.get(f"{BASE_URL}/upload/history", headers=headers)
    if r.status_code == 200:
        uploads = r.json()
        record_test("Upload History Retrieval", True, f"{len(uploads)} files")
        
        if uploads:
            print(f"\n   📁 Recent Uploads:")
            for upload in uploads[:3]:
                print(f"      - {upload.get('filename')}: {upload.get('total_rows', 0)} rows, ${upload.get('total_revenue', 0):,.2f}")
    else:
        record_test("Upload History Retrieval", False, r.json())
except Exception as e:
    record_test("Upload History Retrieval", False, str(e))

# ============================================================================
# FINAL RESULTS
# ============================================================================
print_section("📊 FINAL TEST RESULTS")

total_tests = results["passed"] + results["failed"]
pass_rate = (results["passed"] / total_tests * 100) if total_tests > 0 else 0

print(f"\n   Total Tests Run: {total_tests}")
print(f"   ✅ Passed: {results['passed']}")
print(f"   ❌ Failed: {results['failed']}")
print(f"   📈 Pass Rate: {pass_rate:.1f}%")

print("\n" + "="*80)

if pass_rate >= 90:
    print("   🎉 EXCELLENT! All major features working perfectly!")
elif pass_rate >= 75:
    print("   ✅ GOOD! Most features working, minor issues detected.")
elif pass_rate >= 50:
    print("   ⚠️  FAIR! Several features need attention.")
else:
    print("   ❌ CRITICAL! Major issues detected.")

print("="*80)

# Detailed failure report
if results["failed"] > 0:
    print("\n📋 Failed Tests Details:")
    for test in results["tests"]:
        if not test["passed"]:
            print(f"   ❌ {test['name']}: {test['details']}")

print("\n✅ Testing Complete!\n")
