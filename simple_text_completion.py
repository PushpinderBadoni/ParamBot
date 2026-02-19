"""

A minimal example that shows how to use the OpenAI Chat API
and what each role (system, user, assistant) means.

Roles:
- system: sets overall behavior or tone of the model
- user:   what the human asks or requests
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")



client = OpenAI(api_key=api_key)

# ----------------------------
# Example conversation setup
# ----------------------------
messages = [
    {
        "role": "system",
        "content": "You are a friendly tutor who explains things simply."
    },
    {
        "role": "user",
        "content": "Explain what machine learning is in one short paragraph."
    }
]

# ----------------------------
# Send the request
# ----------------------------
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    temperature=0.3,
    max_tokens=100
)

# ----------------------------
# Print the model’s reply
# ----------------------------
print("\nAssistant:\n")
print(response.choices[0].message.content)