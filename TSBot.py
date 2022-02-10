import discord
from discord.ext import commands
import sqlite3
import youtube_dl
import os
from googleapiclient.discovery import build
import random
import numpy as np




os.system("pip3 install lavalink")
os.system("pip3 install dismusic")
bot = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())





api_key = 'AIzaSyAOwnf58KPpWpYQ1rwkSfjgtuNDiJmp1xA'



@bot.event
async def on_ready():
	db = sqlite3.connect('main.sqlite')
	cursor = db.cursor()
	cursor.execute('''
	  CREATE TABLE IF NOT EXISTS main(
	  guild_id TEXT,
	  msg TEXT,
	  channel_id TEXT
	  )
		''')
	print("Bot was connected to the server")

   
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("$help")) # Изменяем статус боту$

@bot.command( pss_context = True )


async def say   ( ctx, *, message ):
	await ctx.message.delete()
	embed = discord.Embed(
		title= f"{message}", color = discord.Color.blue()
	)

	await ctx.send(embed=embed)


@bot.command()
async def help(ctx):

	embed = discord.Embed(
		title="💼Commands",
		description="🔎Here you can find the necessary command🔎",
		color = discord.Color.blue()
	)
	commands_list = ["$say", "$clear", "$kick", "$donate", "$mute","$play name a sound", "$stop",'$show name image']
	descriptions_for_commands = ["🤖Make the bot talk!🤖", "🚰Clears the chat🚰", "❌Kick a user!❌", '💰Show donation links💰', '🤐mute the user 🤐', '♪Play a music!♪','♪Stop a sound♪', '🔎search image in google🔎']

	for command_name, description_command in zip(commands_list, descriptions_for_commands):
		embed.add_field(
			name=command_name,
			value=description_command,
			inline=False # Будет выводиться в столбик, если True - в строчку
		)

	await ctx.send(embed=embed)


	
@bot.command(name="mute", brief="Запретить пользователю писать", usage="mute <member>")
async def mute_user(ctx, member: discord.Member):
	mute_role = discord.utils.get( ctx.message.guild.roles, name="Mute" )

	await member.add_roles( mute_role )
	await ctx.send(f"{ctx.author} gave role mute to {member}")



@bot.command(name="clear", brief="Очистить чат от сообщений, по умолчанию 10 сообщений", usage="clear <amount=10>")
async def clear(ctx, amount: int=10):
	await ctx.channel.purge(limit=amount)
	await ctx.send(f"Was deleted {amount} messages...")


#Kick
@bot.command( pss_context = True )
async def kick( ctx, member: discord.Member, *, reason= None ):
	await ctx.channel.purge( limit = 1 )

	await member.kick( reason = reason )
	await ctx.send(f'kick user { member.mention }')
@bot.command( pss_context = True )
async def ban( ctx, member: discord.Member, *, reason= None ):
	await ctx.channel.purge( limit = 1 )

	await member.ban( reason = reason )
	await ctx.send(f'ban user { member.mention }')

@bot.command()  
async def donate( ctx ):
	embed = discord.Embed(
		title="💰DONATE LINK💰",
		description=' 👩🏿‍💻Link https://www.donationalerts.com/r/hippi_games_tv '
	)
	
	



	await ctx.send(embed=embed)

channels_count = 0
for guild in bot.guilds:
    channels_count += len(guild.channels)
 

@bot.command()
async def poop(ctx):
 await ctx.send(':poop:')

@bot.event
async def on_command_error(ctx, error):
	print(error)

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
	elif isinstance(error, commands.UserInputError):
		await ctx.send(embed=discord.Embed(
			description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
		))

@bot.command(aliases=["show"])
async def showpic(ctx,*, search):
  ran = random.randint(0,9)
  resource = build('customsearch','v1', developerKey=api_key).cse()
  result = resource.list(q=f'{search}', cx='9ba6f87c309cc2e15', searchType='image').execute()
  url = result["items"][ran]["link"]
  embed1 = discord.Embed(title=f'Here you image ({search.title()})' )
  embed1.set_image(url=url)
  await ctx.send(embed=embed1)

@bot.command()
async def info():
  embed2 = discord.Embed()
