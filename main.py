import discord
import logging
import time
import os
import auth


LOG_CHANNEL_ID="" #TODO: export this to a config file somewhere
EDITS_CHANNEL_ID=""

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

    if msg_old.content != msg_new.content: # Otherwise it will trigger with embeds (like links)
        embed_message = discord.Embed(title="A message was edited!", \
            description="**Timestamp:** {time}\n**User:** {user}\n**Channel:** {channel}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y'), user=msg_old.author, channel=msg_old.channel.name), color=0xffbf00)
        embed_message.add_field(name="Before:", value=msg_old.content, inline=False)
        embed_message.add_field(name="After:", value=underliner(msg_old.content, msg_new.content), inline=False)
        await client.send_message(discord.Object(id=EDITS_CHANNEL_ID), embed=embed_message)


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
             

@client.event
async def on_channel_create(channel):
    """Logs created channels."""

    embed_message = discord.Embed(title="A channel was created!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x90f550)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The channel {name} has been created.".format(name=channel.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_channel_delete(channel):
    """Logs deleted channels."""

    embed_message = discord.Embed(title="A channel was deleted!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x12ad2a)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The channel {name} has been deleted.".format(name=channel.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_channel_update(old_channel, new_channel):
    """Logs modified channels."""

    embed_message = discord.Embed(title="A channel was modified!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x66d13e)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The channel {name} has been modified.".format(name=old_channel.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)

       
@client.event
async def on_member_join(user):
    """Logs new users."""

    embed_message = discord.Embed(title="A new user joined the server!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x59dbf1)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The user {nick} with ID {id_number} has joined the server.\
            \nThe account was created at {register}.".format(nick=user.name, id_number=user.id, register=user.created_at), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)

       
@client.event
async def on_member_remove(user):
    """Logs users that leave."""

    embed_message = discord.Embed(title="An user left the server!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x0052a5)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The user {name}, known in the server as {nick}, with ID {id_number} has left the server."\
            .format(nick=user.nick, name=user.name, id_number=user.id), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)

       
@client.event
async def on_member_update(old_user, new_user):
    """Logs user modifications (mainly new aliases)."""

    embed_message = discord.Embed(title="An user has been modified!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x413bf7)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The user {name}, known in the server as {nick}, with ID {id_number} has been modified."\
            .format(nick=old_user.nick, name=old_user.name, id_number=old_user.id), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_server_role_create(role):
    """Logs new roles."""
    
    embed_message = discord.Embed(title="A role was created!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0xb564e3)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The role {name} has been created.".format(name=role.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)

   
@client.event
async def on_server_role_delete(role):
    """Logs deleted roles."""
 
    embed_message = discord.Embed(title="A role was deleted!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x9600cd)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The role {name} has been deleted.".format(name=role.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_server_role_update(old_role, new_role):
    """Logs role modifications."""
    
    embed_message = discord.Embed(title="A role was modified!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0xa442dc)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The role {name} has been modified.".format(name=old_role.name), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_member_ban(user):
    """Logs banned users."""
 
    embed_message = discord.Embed(title="An user has been banned from the server!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0xffffff)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The user {name}, known in the server as {nick}, with ID {id_number} has been banned from the server."\
            .format(nick=user.nick, name=user.name, id_number=user.id), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


@client.event
async def on_member_unban(user):
    """Logs unbanned users."""
 
    embed_message = discord.Embed(title="A role was deleted!", \
            description="**Timestamp:** {time}".format(\
            time=time.strftime('%l:%M%p %Z on %b %d, %Y')), color=0x000000)
    embed_message.add_field(name="￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣", value="The user {name} with ID {id_number} has been unbanned from the server."\
            .format(name=user.name, id_number=user.id), inline=False)
    await client.send_message(discord.Object(id=LOG_CHANNEL_ID), embed=embed_message)


def underliner(old_content, new_content):
    """Underlines all the changes in the new message for easy change recognition."""
    old_list = old_content.split(" ")
    new_list = new_content.split(" ")
    if len(old_list) >= len(new_list):
        for word in range(len(new_list)):
            if old_list[word] != new_list[word]:
                new_list[word] = "__" + new_list[word] + "__"
    else:
        for word in range(len(old_list)):
            if old_list[word] != new_list[word]:
                new_list[word] = "__" + new_list[word] + "__"

    underlined_content = " ".join(new_list)
    return underlined_content


# Start Bot
client.run(auth.bot_token)
