import discord
from discord.ext import commands
import credits as cr
from deadlock_api import DeadlockApi

api = DeadlockApi()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def last_match(ctx, steam_id):
    stats = await api.get_player_match_history(steam_id)

    if not stats:
        await ctx.send('Ошибка')
        return
    
    message = f'{stats['match_id']}, {stats['hero']}, {stats['kills']}, {stats['deaths']}, {stats['result']}'
    await ctx.send(message)

bot.run(cr.TOKEN)