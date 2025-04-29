import os
import requests

class OpenRouterAPI:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        if not self.api_key:
            raise ValueError("OpenRouter API key not found in environment variables")

    def generate_text(self, prompt, model='gpt-4o-mini', max_tokens=500):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']

# Example usage:
# openrouter = OpenRouterAPI()
# result = openrouter.generate_text("Generate a book outline about psychology for Gen Z")
# print(result)