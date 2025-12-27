import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

# Initialize client
client = OpenAI(api_key=api_key)
# This code will work if your .env file contains a line like:
# OPENAI_API_KEY=your_actual_api_key_here
# Make sure the .env file is in the same directory as main.py and contains your valid API key.
def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
        print("Session ended. Goodbye!")