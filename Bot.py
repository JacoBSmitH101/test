# Imports
import time

import discord
import trainInfo
from discord.ext import commands
from discord.voice_client import VoiceClient
import requests
import asyncio
import config
import json

# Variables
bot = commands.Bot(command_prefix='ned')
channel = bot.get_channel('762345640733966341')
waitForResponse = False


# Opening Files
def joinVoiceChannel():
    print('Bot should joined the Channel')


# Commands / Events
@bot.command(pass_context=True)
async def info(ctx):
    embed = discord.Embed(color=0xff7171)
    embed.add_field(name="Python", value="3.6.4", inline=True)
    embed.add_field(name="discord.py", value="1.0.0a", inline=True)
    embed.add_field(name="About BlueTemp",
                    value="This is an instance of BlueTemp, an open sorce Discord Bot created by RedstonedLife",
                    inline=False)
    embed.set_footer(text="A Template downloaded from Github")
    await ctx.send(embed=embed)


def setTrue():
    waitForResponse = True


@bot.event
async def on_ready():
    waitForResponse = False
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you breath"))
    print(bot.user.id)
    print("---------------------------------------------------------------------")


@bot.event
async def on_message(message: discord.Message):
    content = message.content.lower().split(' ')

    if not waitForResponse:
        if message.author == bot.user:
            print("BOT")
        elif content[0] == 'ned':
            if content[1:]:
                if content[1] == 'get' and content[2] == 'info':
                    await message.channel.send("Getting Info(10 seconds)")

                    time.sleep(10)
                    trainInfo.getCnmInfoNow()
                    with open('Discord.Py-Bot-Template-master/output.txt', 'r') as file:

                        channel = bot.get_channel(763646315426218024)

                        await channel.send(file.read())
                        # for line in file:
                        #   if line != '\n':
                        #     await message.channel.send(line)
                elif content[1] == 'say':
                    await message.delete()
                    x = 2
                    newMessage = ''
                    while x < len(content):
                        newMessage += ' ' + content[x]
                        x += 1
                    await message.channel.send(newMessage)
                elif content[1] == 'whoami':
                    await message.channel.send(message.author)
        else:
            if content[0] == 'hello' and content[1] == 'ned':
                await message.channel.send("Hello how are you")
                setTrue()
    else:
        print("LIT")
        await message.channel.send("Ok cool")


bot.run("NzYyMzQyNTI2MDUxOTQyNDIy.X3nwzQ.1UMEYXH6oXo1Lgn1z5YxO5_lT9c")
