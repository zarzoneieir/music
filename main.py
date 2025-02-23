import disnake
from disnake.ext import commands
import os
import asyncio
import random
import config

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)
guild = disnake.utils.get(bot.guilds, id=1246810383000404019)
news_channel = disnake.utils.get(guild.text_channels, id=1246810383956578336)

# Play Music
@bot.slash_command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client

    if not voice_client:
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        return await ctx.send("Бот уже подключен к другому каналу!")

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    if 'm' in url:
        mp3_path = "downloads\\mazelov.mp3"
    elif 'f' in url:
        mp3_path = "downloads\\fimozik.mp3"
    elif 'sdeti' in url:
        mp3_path = "downloads\\sdeti.mp3"
    elif 'hh' in url:
        mp3_path = "downloads\\hh.mp3"
    else:
        mp3_path = f"downloads/{url.split('/')[-1]}.mp3"

    if not os.path.exists(mp3_path):
        return await ctx.send("Не удалось найти аудио файл.")

    await ctx.response.defer(ephemeral=True)
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.edit_original_response(content="🎶 Воспроизведение начато!")

# Stop Music
@bot.slash_command()
async def stop(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Бот отключился!")

# Timur Huesos Command
@bot.slash_command()
async def timur_huesos(ctx):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client or await channel.connect()

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    mp3_path = "downloads\\huesos.mp3"

    if not os.path.exists(mp3_path):
        return await ctx.send("Не удалось найти аудио файл.")

    await ctx.response.defer(ephemeral=True)
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.edit_original_response(content="🎶 Воспроизведение начато!")

# BBW Command
@bot.slash_command()
async def bbw(ctx):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.guild.voice_client or await channel.connect()

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    mp3_path = "downloads\\bbv.mp3"

    if not os.path.exists(mp3_path):
        return await ctx.send("Не удалось найти аудио файл.")

    await ctx.response.defer(ephemeral=True)
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.edit_original_response(content="🎶 Воспроизведение начато!")

# Moderation Commands
@bot.slash_command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был исключен из сервера. Причина: {reason}")

@bot.slash_command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} был забанен. Причина: {reason}")

# Partner Management
@bot.slash_command()
async def partner(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=1246810383034093670)
    if role:
        await member.add_roles(role)
        await news_channel.send(f"{member.mention}, теперь ты партнер!")
    else:
        await ctx.send("Роль партнера не найдена!")

@bot.slash_command()
async def unpartner(ctx, member: disnake.Member):
    role = disnake.utils.get(ctx.guild.roles, id=1246810383034093670)
    if role:
        await member.remove_roles(role)
        await news_channel.send(f"{member.mention}, теперь ты не партнер!")
    else:
        await ctx.send("Роль партнера не найдена!")

bot.run(config.TOKEN)