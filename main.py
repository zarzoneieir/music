import disnake
from disnake.ext import commands
import config

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)

# ID канала для отправки сообщений
LOG_CHANNEL_ID = 1246810383956578336

# Команда для очистки сообщений
@bot.slash_command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.response.send_message(f"Удалено {amount} сообщений!", ephemeral=True)

# Команда для бана пользователей
@bot.slash_command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, reason: str = "Без причины"):
    await member.ban(reason=reason)
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"Пользователь {member.mention} был забанен! Причина: {reason}")

# Команда для разбанивания пользователей
@bot.slash_command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: str):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        if ban_entry.user.name == user:
            await ctx.guild.unban(ban_entry.user)
            channel = bot.get_channel(LOG_CHANNEL_ID)
            if channel:
                await channel.send(f"Пользователь {user} был разбанен!")
            return
    await ctx.response.send_message(f"Пользователь {user} не найден в списке забаненных.")

# Команда для выдачи партнёра
@bot.slash_command()
async def partner(ctx, member: disnake.Member):
    await ctx.response.defer()
    role = disnake.utils.get(ctx.guild.roles, name="Partner")
    if role:
        await member.add_roles(role)
        channel = bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(f"Пользователю {member.mention} выдана роль Partner!")
    else:
        await ctx.followup.send("Роль Partner не найдена.")

# Команда для снятия роли партнёра
@bot.slash_command()
async def unpartner(ctx, member: disnake.Member):
    await ctx.response.defer()
    role = disnake.utils.get(ctx.guild.roles, name="Partner")
    if role and role in member.roles:
        await member.remove_roles(role)
        channel = bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(f"У пользователя {member.mention} снята роль Partner!")
    else:
        await ctx.followup.send("У пользователя нет роли Partner или роль не найдена.")

bot.run(config.TOKEN)
