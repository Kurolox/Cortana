import discord
import logging
import time
import os
import auth


LOG_CHANNEL_ID="INSERT LOG_CHANNEL_ID HERE" #TODO: export this to a config file somewhere

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

    embed_message = discord.Embed(title="A message was deleted!", \
            description="**Timestamp:** {time}\n**User:** {user}\n**Channel:** {channel}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y'), user=msg.author, channel=msg.channel.name), color=0xff0000)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value=msg.content, inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_message_edit(msg_old, msg_new):

    """Logs edited messages."""
    embed_message = discord.Embed(title="A message was edited!", \
        description="**Timestamp:** {time}\n**User:** {user}\n**Channel:** {channel}".format(\
        time=time.strftime('%l:%M%p %Z on %b %d, %Y'), user=msg_old.author, channel=msg_old.channel.name), color=0xffbf00)
    embed_message.add_field(name="Before:", value=msg_old.content, inline=False)
    embed_message.add_field(name="After:", value=msg_new.content, inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_message(msg):
    """Logs all messages locally."""

    while True:
        try:
            with open(os.path.dirname(os.path.realpath(__file__)) + "/logs/" + time.strftime("%Y-%m-%d", time.localtime(time.time())), "a") as log: # Open log file at /logs
                timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) #Ex: 1990-04-14 15:23:52
                log.write("%s %s [%s -> %s]: %s\n" % (timenow, msg.author, msg.server, msg.channel, msg.content))
                break 
        except FileNotFoundError: # If there's no /logs folder
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + "/logs") # Create it and try again
            
# Start Bot
client.run(auth.bot_token)
