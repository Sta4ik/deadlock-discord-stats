import discord
from discord.ext import commands
import credits as cr
from deadlock_api import DeadlockApi
import io

api = DeadlockApi()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='#', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def helpc(ctx):
    embed = discord.Embed(
        title="Список команд бота",
        description="Все команды используют префикс `#`",
        color=discord.Color.gold()
    )
    
    embed.add_field(
        name="#ping",
        value="Проверка работоспособности бота",
        inline=False
    )
    
    embed.add_field(
        name="#last или #last_match [deadlock_id]",
        value="Возвращает информацию о последнем матче игрока\n`Пример: #last 123456`",
        inline=False
    )
    
    embed.add_field(
        name="#getid [steam_id]",
        value="Получает Deadlock ID по SteamID64\n`Пример: #getid 76561198000000000`",
        inline=False
    )
    
    embed.add_field(
        name="#whois [account_id]",
        value="Показывает информацию о Steam профиле по Deadlock ID\n`Пример: #whois 123456`",
        inline=False
    )
    
    embed.add_field(
        name="#lead или #leaderbord [регион]",
        value="Показывает топ-10 игроков в указанном регионе\nДоступные регионы: `Europe`, `Asia`, `NAmerica`, `SAmerica`, `Oceania`\n`Пример: #lead Europe`",
        inline=False
    )
    
    embed.add_field(
        name="#help",
        value="Показывает это сообщение с помощью",
        inline=False
    )
    
    embed.set_footer(text="Deadlock Stater Bot")
    
    await ctx.send(embed=embed)

@bot.command(aliases=["last"])
async def last_match(ctx, deadlock_id=None):
    try:
        if not deadlock_id:
            await ctx.send("Укажите deadlock id")
            return
        
        stats = await api.get_player_last_match(int(deadlock_id))

        if not stats:
            await ctx.send(f'Ошибка получения последнего матча игрока {deadlock_id}')
            return

        hero = await api.get_hero_by_id(stats["hero_id"])

        if not hero:
            await ctx.send(f'Ошибка получения героя с id {stats["hero_id"]}')
            return
        
        hero_name = hero["name"]
        hero_icon = hero["images"]["icon_image_small"]

        is_win = stats["match_result"] == stats["player_team"]
        color = discord.Color.green() if is_win else discord.Color.red()
        result = "Победа" if is_win else "Поражение"

        duration_min = stats["match_duration_s"] // 60
        duration_sec = stats["match_duration_s"] % 60

        embed = discord.Embed(
            title=f"Последний матч игрока {deadlock_id}",
            description=f"**{hero_name}**",
            color=color
        )

        embed.set_thumbnail(url=hero_icon)

        embed.add_field(name="Матч ID", value=stats["match_id"], inline=False)
        embed.add_field(name="K/D/A", value=f"{stats['player_kills']}/{stats['player_deaths']}/{stats['player_assists']}", inline=True)
        embed.add_field(name="Нетворс", value=stats["net_worth"], inline=True)
        embed.add_field(name="Длительность", value=f"{duration_min}:{duration_sec} мин", inline=True)

        embed.add_field(name="Команда", value=("The Hidden King" if stats["player_team"] == 0 else "The ArchMother"), inline=True)
        embed.add_field(name="Результат", value=result, inline=True)

        embed.set_footer(text="Deadlock stater")

        await ctx.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await ctx.send(f'Ошибка получения последнего матча игрока {deadlock_id}')

@bot.command(aliases=["getid"])
async def get_id(ctx, steam_id=None):
    try:
        if not steam_id:
            await ctx.send("Укажите SteamID64")
            return
        
        id = await api.get_id_by_steam_id(int(steam_id))
        
        if not id:
            await ctx.send(f"Ошибка получения deadlock id с Steam id {steam_id}")
            return
        
        await ctx.send(id)

    except Exception as e:
        print("Error:", e)
        await ctx.send(f"Ошибка получения deadlock id с Steam id {steam_id}")

@bot.command(aliases=["whois"])
async def who_is(ctx, account_id=None):
    try:
        if not account_id:
            await ctx.send("Укажите deadlock id")
            return
        
        steam_info = await api.get_steam_profile_by_id(int(account_id))

        if not steam_info:
            await ctx.send(f"Ошибка получения стим профиля с deadlock id {account_id}")
            return

        embed = discord.Embed(
            title=steam_info["name"],
            url=steam_info["steam_url"],
            color=discord.Color.blue()
        )

        embed.set_thumbnail(url=steam_info["avatar"])
        embed.add_field(name="Настоящее имя", value=steam_info["realname"] or "Не указано", inline=False)
        embed.add_field(name="Матчей за 30 дней", value=steam_info["matches_played_last_30d"], inline=True)

        rank_image = await api.get_rank_image(int(account_id))
        if rank_image:
            file = discord.File(io.BytesIO(rank_image), filename="rank.png")
            embed.set_image(url="attachment://rank.png")
            await ctx.send(embed=embed, file=file)
        else:
            await ctx.send(embed=embed)


    except Exception as e:
        print("Error:", e)
        await ctx.send(f"Ошибка получения стим профиля с deadlock id {account_id}")

@bot.command(aliases=["lead"])
async def leaderbord(ctx, region=None):
    try:
        if not region:
            await ctx.send("Укажите регион (Europe, Asia, NAmerica, SAmerica, Oceania)")
            return
        
        leaderbord = await api.get_leaderboard(region)

        if not leaderbord:
            await ctx.send(f"Ошибка получения лидерборда региона {region}")
            return
        
        message = ""
        for i in range(0, 10):
            message += f"{i + 1} - {leaderbord[i]['account_name']}\n"

        await ctx.send(message)

    except Exception as e:
        print("Error:", e)
        await ctx.send(f"Ошибка получения лидерборда региона {region}")

if __name__ == "__main__":
    bot.run(cr.TOKEN)