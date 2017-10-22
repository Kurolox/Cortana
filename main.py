import discord
import logging
import time
import os
import auth

# Enable logging
logging.basicConfig(level=logging.INFO)

# Generate client
client = discord.Client()

@client.event
async def on_ready():
    """Outputs some info at the console and sets the game of the bot."""

    await client.change_presence(game=discord.Game(name="with telemetry"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message_delete(msg):
    """Logs removed messages."""

@client.event
async def on_message_edit(msg):
    """Logs edited messages."""


# Start Bot
client.run(auth.bot_token)
