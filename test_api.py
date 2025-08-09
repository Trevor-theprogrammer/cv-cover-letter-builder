from openai import OpenAI
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')

try:
    # Create a custom http client without proxy
    http_client = httpx.Client(proxy=None)
    client = OpenAI(
        api_key=api_key,
        http_client=http_client
    )
    
    # Try a simple API call
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}],
        max_tokens=5
    )
    print("API Key is working correctly!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error testing API key: {str(e)}")
