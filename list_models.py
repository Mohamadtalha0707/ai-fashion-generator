import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyDAbwn8av6bI7VoYlYYuz-HSgR_ygbdc9U")

# List available models
print("Available models that support generateContent:\n")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")