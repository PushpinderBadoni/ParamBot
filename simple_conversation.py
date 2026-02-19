#!/usr/bin/env python3
"""
PUSHPINDER BADONI , 000916094 AND 6TH NOVEMBER,2025

"""
"""
Developed by Amin Azmoodeh - Fall 2025


A simple chatbot example using OpenAI API that remembers the conversation.

How it works:
- The conversation is stored in a list called `messages`.
- Each turn adds the user's input (role="user")
  and the assistant's reply (role="assistant").
- The model sees the full conversation every time.

To stop chatting, type 'exit' or 'quit'.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": (
            "You are a friendly bot."
            "You are only supposed to reply to questions related to programming and coding."
            "Give a positive response to all other types of questions saying that it is out of your knowledge area."
            "If there is any kind of greeting, then reply appropriately"
            "Always explain concepts clearly and simply."
            "Remember the conversation context."
            "Consider previous user prompts and their response to generate new response to new input, be in context of conversation."
        ),
    }
]

# ----------------------------
# Initial system instruction
# ----------------------------
def generate_response(user_input):


    messages.append({"role": "user", "content": user_input})

        # Get model response with temperature 0.6 for more accuracy
    response1 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.6,
        max_tokens=800
    )

        # Get model response with temperature 0.9 for more creativity
    response2 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.9,
        max_tokens=800
    )


        # Extract the assistant reply for both responses
    reply1 = response1.choices[0].message.content.strip()
    reply2 = response2.choices[0].message.content.strip()
    # Show reply

    evaluation_prompt=[{
            "role": "system",
            "content": (
                "You are an expert evaluator."
                "You will be given two responses from another AI. "
                "Compare them. You have to either choose the better one or combine them both to generate a better response."
                "You are not allowed to add your own content to the responses provided."
                "Form a single, clear, and accurate final answer."
            )
        },
        {
            "role": "user",
            "content": (
                f"User question: {user_input}\n\n"
                f"Response A:\n{reply1}\n\n"
                f"Response B:\n{reply2}\n\n"
                "Now provide the best or merged both responses."
        )
    }]


        #Evaluating both the initial responses and forming a final response
    evaluate_response = client.chat.completions.create(
        model="gpt-4o", #Validating initial responses by inferior model on a superior model
        messages=evaluation_prompt,
        temperature=0.5,   #Low randomness for consistency
        max_tokens=800
    )

    final_reply = evaluate_response.choices[0].message.content.strip()

    messages.append({"role": "assistant", "content": final_reply})
    return final_reply



def main():
    """Implements a chat session in the shell."""
    print("Hi! I am your Assistant Software Developer, here to help you with coding. Type 'exit' or 'quit' to stop.\n")
    print()
    utterance = ""
    while True:
        #utterance is the user input - what user chats with bot
        utterance = input(">>> ")
        utterance=utterance.lower()
        if utterance in {"exit", "quit"}:
            print("Goodbye!")
            break;

#intent is the index question which matches the utterance. further use the intent to generate response

        response = generate_response(utterance) #modified generate - additional argument utterance passed

        print(response)
        print()

    print("Nice talking to you!")

## Run the chat code
# the if statement checks whether or not this module is being run
# as a standalone module. If it is beign imported, the if condition
# will be false and it will not run the chat method.
if __name__ == "__main__":
    main()