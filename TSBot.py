import discord
from discord.ext import commands
import sqlite3
import youtube_dl
import os
import json
import asyncio
import asyncpraw
import config


bot = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())
reddit = asyncpraw.Reddit(client_id=config.settings['CLIENT_ID'],
	client_secret=config.settings['SECRET_CODE'],
	user_agent='rendom_reddit_bot/0.0.1'
	)
memes = []
TIMEOUT = 5
ID_CHANNEL = 932748473424564224
SUBREDDIT_NAME = 'memes'
POST_LIMIT = 1




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
	channel = bot.get_channel(ID_CHANNEL)
	while True:
		await asyncio.sleep(TIMEOUT)
		memes_submissions = await reddit.subreddit(SUBREDDIT_NAME)
		memes_submissions = memes_submissions.new(limit=POST_LIMIT)
		item = await memes_submissions.__anext__()
		if item.title not in memes:
			memes.append(item.title)
			await channel.send(item.url)

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
		description="🔎Here you can find the necessary command🔎"
	)
	commands_list = ["$say", "$clear", "$kick", "$donate", "$mute","$play", "$stop"]
	descriptions_for_commands = ["🤖Make the bot talk!🤖", "🚰Clears the chat🚰", "❌Kick a user!❌", '💰Show donation links💰', '🤐mute the user 🤐', '♪Play a music!♪','♪Stop a sound♪']

	for command_name, description_command in zip(commands_list, descriptions_for_commands):
		embed.add_field(
			name=command_name,
			value=description_command,
			inline=False # Будет выводиться в столбик, если True - в строчку
		)

	await ctx.send(embed=embed)


	
@bot.command(name="mute", brief="Запретить пользователю писать (настройте роль и канал)", usage="mute <member>")
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
		title="💰DONATE LINK",
		description=' 👩🏿‍💻Link https://www.donationalerts.com/r/hippi_games_tv '
	)
	
	



	await ctx.send(embed=embed)

channels_count = 0
for guild in bot.guilds:
    channels_count += len(guild.channels)

@bot.command()
async def botservers():
	guilds_count = len(bot.guilds)

@bot.command()
async def pop(ctx):
	await ctx.send('💩')



token = open( 'token.txt', 'r' ).readline()

bot.run( token )
