import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix="$", help_command=None, intents=discord.Intents.all())



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


async def say	( ctx, arg ):
	author = ctx.message.author

	await ctx.send( f' { author.mention } ' + arg )

@bot.command()
async def help(ctx):

	embed = discord.Embed(
		title="Commands",
		description="Here you can find the necessary command"
	)
	commands_list = ["$say", "$clear", "$kick"]
	descriptions_for_commands = ["Make the bot talk!", "Clears the chat", "Kick a user!"]

	for command_name, description_command in zip(commands_list, descriptions_for_commands):
		embed.add_field(
			name=command_name,
			value=description_command,
			inline=False # Будет выводиться в столбик, если True - в строчку
		)

	await ctx.send(embed=embed)


    
@bot.command(name="mute", brief="Запретить пользователю писать (настройте роль и канал)", usage="$mute <member>")
async def mute_user(ctx, member: discord.Member):
	mute_role = discord.utils.get(ctx.message.guild.roles, name="role name")

	await member.add_roles(mute_role)
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


token = open( 'token.txt', 'r' ).readline()

bot.run( token )
