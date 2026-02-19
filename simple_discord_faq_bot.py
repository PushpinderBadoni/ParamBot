"""
PUSHPINDER BADONI , 000916094 AND 6TH NOVEMBER,2025

"""
import discord
import asyncio
import nest_asyncio
from simple_conversation import generate_response

## MYClient Class Definition

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        # get the utterance and generate the response
        user_input = message.content.strip()
        #asyncronosly generating response to maintain the discord bot heartbeat
        try:
            response = await asyncio.to_thread(generate_response, user_input)
        except Exception as e:
            await message.channel.send(f"Error while generating response: {e}")

        # send the response, Discord limits the response to 2000 characters so converting the response into chunks if needed
        if len(response) > 2000:
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await message.channel.send(chunk)
        else:
            await message.channel.send(response)


## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()
# ---- Fix for Pyzo - Pyzo runs an event loop which stops my code from working on my personal Pyzo, so imported nest_asyncio to escape that ----
nest_asyncio.apply()

async def main():
    await client.start(token)

asyncio.get_event_loop().run_until_complete(main())
