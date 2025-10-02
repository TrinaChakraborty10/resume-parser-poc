import requests
import os

def test_resume_parser_api():
    """Test the FastAPI resume parser endpoints"""
    
    # API base URL
    base_url = "http://localhost:8000"
    
    # Test resume file path
    resume_path = "C:/Users/10723269/Downloads/AniruddhaLaha_resume.pdf"
    
    print("🚀 Testing Resume Parser API")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(base_url)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Upload resume endpoint
    print("\n3. Testing resume upload endpoint...")
    if os.path.exists(resume_path):
        try:
            with open(resume_path, 'rb') as file:
                files = {'file': (os.path.basename(resume_path), file, 'application/pdf')}
                response = requests.post(f"{base_url}/upload-resume", files=files)
                
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print("   ✅ Success! Extracted data:")
                    print(f"   📄 Filename: {data.get('filename')}")
                    print(f"   👤 Name: {data['extracted_data'].get('name')}")
                    print(f"   📧 Email: {data['extracted_data'].get('email')}")
                    print(f"   📱 Phone: {data['extracted_data'].get('mobile_number')}")
                    print(f"   🎓 Degree: {data['extracted_data'].get('degree')}")
                    print(f"   🏢 Skills: {data['extracted_data'].get('skills', [])[:5]}...")  # Show first 5 skills
                else:
                    print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    else:
        print(f"   ⚠️  Resume file not found: {resume_path}")
    
    # Test 4: Detailed parse endpoint
    print("\n4. Testing detailed parse endpoint...")
    if os.path.exists(resume_path):
        try:
            with open(resume_path, 'rb') as file:
                files = {'file': (os.path.basename(resume_path), file, 'application/pdf')}
                response = requests.post(f"{base_url}/parse-resume", files=files)
                
                print(f"   Status Code: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print("   ✅ Success! Categorized data:")
                    print(f"   Personal Info: {data.get('personal_info')}")
                    print(f"   Education: {data.get('education')}")
                    print(f"   Professional Skills: {len(data.get('professional', {}).get('skills', []))} skills found")
                else:
                    print(f"   ❌ Error: {response.text}")
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n🎉 API Testing Complete!")
    print(f"💡 You can also test the API at: {base_url}/docs (Swagger UI)")

if __name__ == "__main__":
    test_resume_parser_api()