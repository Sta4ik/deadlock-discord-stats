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
async def last_match(ctx, deadlock_id):
    stats = await api.get_player_last_match(int(deadlock_id))

    if not stats:
        await ctx.send('Ошибка')
        return
    
    message = (
        f"Матч: {stats['match_id']}\n"
        f"Герой: {stats['hero_id']}\n"
        f"Убийства: {stats['player_kills']}\n"
        f"Смерти: {stats['player_deaths']}\n"
        f"Результат: {stats['match_result']}"
    )
    await ctx.send(message)

bot.run(cr.TOKEN)