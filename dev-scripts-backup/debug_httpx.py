import httpx
import inspect

try:
    # Get the signature of the httpx.Client initializer
    sig = inspect.signature(httpx.Client.__init__)
    
    print("🔍 Inspecting httpx.Client.__init__ signature...")
    print(f"   {sig}")
    
    # Check if 'proxies' is a valid parameter
    if 'proxies' in sig.parameters:
        print("✅ 'proxies' is a valid parameter for httpx.Client.")
    else:
        print("❌ 'proxies' is NOT a valid parameter for httpx.Client.")
        
except Exception as e:
    print(f"An error occurred during inspection: {e}")
