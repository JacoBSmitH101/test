#This is a command example that you can use to add your own commands to this Template!
#
#Just remember remove the # cause then it won't read the command cause it will be recognized as a comment :D

#The following command is simply a command that takes a number (value) and add 1 to it
import discord
import requests

from Ned import bot


@bot.command(pass_context=True)
async def CommandName(ctx, num):
  num+= 1
  print(num)
  #To message num do
  ctx.send(num)
  
  
#The following command will request a name from a site, Basically a Random Nick. also don't froget to import random
import random
word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(word_site)
@bot.command(pass_context=True)
async def CommandName(ctx, member : discord.Member):
  new_nick = random.choice(response.content.splitlines()).decode("utf-8")
  await member.edit(nick = new_nick)
  
#The following command will let you send Embed messages :D
@bot.command(pass_context=True)
async def CommandName(ctx, embed=None):
  #Use https://cog-creators.github.io/discord-embed-sandbox/ to generate Embed messages!
  #Then simply instead of await self.bot.say(embed=embed) use await ctx.send(embed=embed)
  ctx.send(embed=embed)
