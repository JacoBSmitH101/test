import discord
from discord.ext.commands import Bot
from discord.ext import commands
import main
import time
import asyncio
import os
TOKEN = 'NzYyMzQyNTI2MDUxOTQyNDIy.X3nwzQ.1UMEYXH6oXo1Lgn1z5YxO5_lT9c'
bot = commands.Bot(command_prefix='.')
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command()
async def ping(ctx):
    '''
    This text will be shown in the help command
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('How are you nerdy'):
        await message.channel.send('I am ready to take over the world!!!!!')
    if message.content.startswith('Hello'):
        await message.channel.send('You called for me')
    if message.content.startswith('god damn it ned'):
        await message.channel.send('Dont talk to me like that')
    if message.content.startswith('die'):
        await message.channel.send('This is a christian server please keep it appropriate')
    if message.content.startswith('gimme the tea neddy'):
        await message.channel.send('Getting Tea(could take a while)')

        main.getInfoStandard()
        time.sleep(10)
        try:
            f = open("output.txt", 'r')
        except:
            await message.channel.send("No Trains this Hour")
        if os.path.getsize('output.txt') == 0:
            await message.channel.send("No Trains this Hour")
        else:
            for line in f:
                if line == '\n':
                    print("TESTING")
                    pass
                else:
                    await message.channel.send(line)





client.run(TOKEN)