import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv('OPENAI_API_KEY')
print(f"Attempting to initialize OpenAI client...")
print(f"API Key found: {bool(api_key)}")

if api_key:
    try:
        # Initialize the client
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully!")

        # Make a test request
        print("Making a test API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ Test API call successful!")

    except Exception as e:
        print(f"❌ Error during OpenAI initialization or API call: {e}")
else:
    print("❌ OPENAI_API_KEY not found in environment.")
