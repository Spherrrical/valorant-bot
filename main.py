import discord
from discord.ext import commands, tasks
import os
import random
import json
import keep_alive
import datetime
import asyncio
from itertools import cycle
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from keep_alive import keep_alive













file = discord.File("imgs/logos/valorant.png", filename="valorant.png")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = commands.Bot(command_prefix = ">", intents = intents)
client.remove_command("help")
status = cycle(['help'])
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=">help | v1.0"))
    print("Bot is ready!")
  
@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity = (discord.Activity(type=discord.ActivityType.watching, name= next(status))))
guild_ids = []

@client.event
async def on_guild_join(guild):
  em = discord.Embed(title = "**Thanks for adding me!**", color = discord.Color.red())
  em.add_field(name = "Commands:", value = "`>help` \nThis command will show you all the commands available to use.", inline = False)
  em.add_field(name = "Bot down? Check these links:", value = "\n\n[Status Checker](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n[VALORANT API Status](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline = False)
  em.set_thumbnail(url = "https://cdn.discordapp.com/attachments/807529622530555916/864372137690398780/V_Logomark_Red.png")
  await (guild.text_channels[0]).send(embed = em)

@client.command()
async def help(ctx, *, args = None):
  em = discord.Embed(title = "**Command List**", color = discord.Color.red())
  em.add_field(name = "Commands:", value = "`>help` \nThis command will show you all the commands available to use.", inline = False)
  em.set_thumbnail(url = "https://cdn.discordapp.com/attachments/807529622530555916/864372137690398780/V_Logomark_Red.png")
  await ctx.send(embed = em)

@client.command()
async def welcomemsg(ctx, *, args = None):
  em = discord.Embed(title = "**Thanks for adding me!**", color = discord.Color.red())
  em.add_field(name = "Commands:", value = "`?help` \nThis command will show you all the commands available to use.", inline = False)
  em.add_field(name = "Bot down? Check these links:", value = "\n\n[Status Checker](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n[VALORANT API Status](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline = False)
  em.set_thumbnail(url = "https://cdn.discordapp.com/attachments/807529622530555916/864372137690398780/V_Logomark_Red.png")
  await ctx.send(embed = em)

@client.command()
async def stats(ctx,username: str,tag: str):

  if ' ' in username:
    username.replace(" ", "%20")
  URL = f"https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?playlist=competitive&season=all"
  URL2 = f"https://tracker.gg/valorant/profile/riot/{username}%23{tag}/overview?playlist=competitive"
  page = requests.get(URL, URL2)
  soup = BeautifulSoup(page.content,"html.parser")
  results = soup.find("span", {"class":"valorant-highlighted-stat__value"})
  rank = results.text

  embed=discord.Embed(title=f"Information for {username}#{tag}", color = discord.Color.red())
  embed.add_field(name=f"Rank:" , value=f"**{rank}**")
  embed.set_footer(text=f"Requested By: {ctx.author}\n[View Full Profile] {URL2}")
  await ctx.send(embed=embed)







@client.command()
async def invite(ctx, *, args = None):
  em = discord.Embed(title = "**Want the bot in your own server?**", color = discord.Color.red())
  em.add_field(name = "Invite Link:", value = "[Invite me!](https://discord.com/oauth2/authorize?client_id=863994374769475604&scope=bot&permissions=2147601480)", inline = False)
  em.add_field(name = "Bot down? Check these links:", value = "\n\n[Status Checker](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n[VALORANT API Status](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", inline = False)
  em.set_thumbnail(url = "https://cdn.discordapp.com/attachments/807529622530555916/864372137690398780/V_Logomark_Red.png")
  await ctx.send(embed = em)



guild_ids = [872271507181699092, 535616979478773774, 727699824970956840]

import ast


def insert_returns(body):
	# Insert return stmt if the last expression is a expression statement
	if isinstance(body[-1], ast.Expr):
		body[-1] = ast.Return(body[-1].value)
		ast.fix_missing_locations(body[-1])

	# For if statements, we insert returns into the body and the orelse
	if isinstance(body[-1], ast.If):
		insert_returns(body[-1].body)
		insert_returns(body[-1].orelse)

	# For with blocks, again we insert returns into the body
	if isinstance(body[-1], ast.With):
		insert_returns(body[-1].body)



@client.command(name="eval", usage="{prefix}eval <code>")
async def eval_(ctx, *, cmd):
	if ctx.author.id not in [
	    494893208065671168
	]:
		return
	"""An owner command to run pieces of code. Made for testing"""
	fn_name = "_eval_expr"

	cmd = cmd.strip("` ")

	# Add a layer of indentation
	cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

	# Wrap in async def body
	body = f"async def {fn_name}():\n{cmd}"

	parsed = ast.parse(body)
	body = parsed.body[0].body

	insert_returns(body)

	env = {
	    'client': ctx.bot,
	    'discord': discord,
	    'commands': commands,
	    'ctx': ctx,
	    '__import__': __import__
	}
	exec(compile(parsed, filename="<ast>", mode="exec"), env)

	result = (await eval(f"{fn_name}()", env))
	return


@eval_.error
async def eval_cmd_error(ctx, error):
	if isinstance(error, commands.NotOwner):
		pass
	else:
		if ctx.author.id == 685158612871545139:

			em = discord.Embed(title="Error",
			                   description=error,
			                   color=discord.Color.red())
			await ctx.send(embed=em)


keep_alive()
client.run(os.getenv("TOKEN"))
