import disnake
from disnake.ext import commands
import os
import asyncio
import random

TOKEN = "MTM0Mjk5OTU4NDM2MzkwNTEwNA.G3_60X.hJep9BrpF_kZ-zofT_I7hSxrEd9tl21wRgp5Dw"

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)

# Play Music
@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client or await channel.connect()

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    # Проверка на "m" и "f" в URL
    if 'm' in url:
        mp3_path = "D:\\Python\\dtio\\mn\\downloads\\mazelov.mp3"
    elif 'f' in url:
        mp3_path = "D:\\Python\\dtio\\mn\\downloads\\fimozik.mp3"
    elif 'sdeti' in url:
        mp3_path = "D:\\Python\\dtio\\mn\\downloads\\sdeti.mp3"
    else:
        mp3_path = f"downloads/{url.split('/')[-1]}.mp3"

    if not os.path.exists(mp3_path):
        await ctx.send("Не удалось найти аудио файл.")
        return

    # Пытаемся воспроизвести MP3 без конвертации в WAV
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.send("🎶 Воспроизведение начато!")


# Stop Music
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Бот отключился!")


# Timur Huesos Command
@bot.command()
async def timur_huesos(ctx):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client or await channel.connect()

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    mp3_path = "D:\\Python\\dtio\\mn\\downloads\\huesos.mp3"

    if not os.path.exists(mp3_path):
        await ctx.send("Не удалось найти аудио файл.")
        return

    # Пытаемся воспроизвести MP3 без конвертации в WAV
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.send("🎶 Воспроизведение начато!")


# BBW Command
@bot.command()
async def bbw(ctx):
    if not ctx.author.voice:
        return await ctx.send("Ты должен быть в голосовом канале!")

    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client or await channel.connect()

    if voice_client.is_playing():
        return await ctx.send("Бот уже что-то воспроизводит!")

    mp3_path = "D:\\Python\\dtio\\mn\\downloads\\bbv.mp3"

    if not os.path.exists(mp3_path):
        await ctx.send("Не удалось найти аудио файл.")
        return

    # Пытаемся воспроизвести MP3 без конвертации в WAV
    voice_client.play(disnake.FFmpegPCMAudio(mp3_path), after=lambda e: print(f"Завершено: {e}"))
    await ctx.send("🎶 Воспроизведение начато!")


# Moderation Commands
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: disnake.Member, *, reason=None):
    """Kick a member from the server."""
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был исключен из сервера. Причина: {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member, *, reason=None):
    """Ban a member from the server."""
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} был забанен. Причина: {reason}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: disnake.Member, duration: int, *, reason=None):
    """Mute a member for a certain duration in minutes."""
    muted_role = disnake.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted", permissions=disnake.Permissions(send_messages=False))
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(muted_role, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f"{member.mention} был замучен на {duration} минут. Причина: {reason}")

    await asyncio.sleep(duration * 60)  # Mute duration in minutes
    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} больше не замучен.")


# Fun Commands

# Fun Command 1: Flip a Coin
@bot.command()
async def flipcoin(ctx):
    """Flip a coin and return either 'Heads' or 'Tails'."""
    result = random.choice(["Heads", "Tails"])
    await ctx.send(f"🪙 Ты подкинул монету, и выпало: {result}")


# Fun Command 2: Say Something Random
@bot.command()
async def say(ctx, *, message: str):
    """Make the bot repeat your message."""
    await ctx.send(message)


# Fun Command 3: 8 Ball (Fortune Telling)
@bot.command()
async def eightball(ctx, *, question: str):
    """Ask the magic 8 ball a question."""
    responses = [
        "Да.",
        "Нет.",
        "Возможно.",
        "Я не уверен.",
        "Спроси позже.",
        "Без сомнений!",
        "Точно да.",
        "Скорее всего нет."
    ]
    response = random.choice(responses)
    await ctx.send(f"Вопрос: {question}\nОтвет: {response}")


# Fun Command 4: Random Number Generator
@bot.command()
async def randnum(ctx, min_num: int, max_num: int):
    """Generate a random number between min_num and max_num."""
    number = random.randint(min_num, max_num)
    await ctx.send(f"Рандомное число между {min_num} и {max_num}: {number}")


# Fun Command 5: Dad Joke
@bot.command()
async def dadjoke(ctx):
    """Send a dad joke."""
    jokes = [
        "Почему программисты так не любят лес? Потому что в лесу всегда много ошибок.",
        "Почему коты не играют в покер? Потому что они всегда блефуют!",
        "Что такое баг в программе? Это когда программа работает так, как надо, а ты не понимаешь, почему."
    ]
    await ctx.send(random.choice(jokes))


# Fun Command 6: Roll a Dice
@bot.command()
async def roll(ctx, sides: int):
    """Roll a dice with the given number of sides."""
    roll_result = random.randint(1, sides)
    await ctx.send(f"🎲 Ты кинул кубик с {sides} гранями, и выпало: {roll_result}")


# Fun Command 7: Riddle
@bot.command()
async def riddle(ctx):
    """Ask a riddle."""
    riddles = [
        ("Что может подняться, но не упасть?", "Твой возраст!"),
        ("Что всегда приходит, но никогда не приходит?", "Завтра!"),
        ("Что можно держать в руках, но нельзя увидеть?", "Тень!")
    ]
    riddle, answer = random.choice(riddles)
    await ctx.send(f"Загадка: {riddle}")
    await ctx.send(f"Ответ: {answer}")


# Fun Command 8: Fortune Cookie
@bot.command()
async def fortune(ctx):
    """Give a fortune cookie message."""
    fortunes = [
        "Твои усилия принесут плоды.",
        "Ожидай удачу в ближайшие дни.",
        "Время для больших перемен.",
        "Скоро тебе повезет, не сдавайся!"
    ]
    await ctx.send(f"🍪 Твое предсказание: {random.choice(fortunes)}")


# Fun Command 9: Compliment
@bot.command()
async def compliment(ctx, member: disnake.Member):
    """Give a compliment to a member."""
    compliments = [
        "Ты замечательный человек!",
        "Ты сегодня выглядишь потрясающе!",
        "Ты заставляешь этот мир лучше!",
        "Твои идеи просто гениальны!"
    ]
    await ctx.send(f"{member.mention}, {random.choice(compliments)}")


# Fun Command 10: Pick a Random Color
@bot.command()
async def color(ctx):
    """Pick a random color."""
    colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A1FF33"]
    color = random.choice(colors)
    await ctx.send(f"🎨 Твой случайный цвет: {color}")


# Custom Help Command
@bot.command()
async def helpan(ctx):
    """Shows the list of available commands."""
    help_text = """
    **Команды для музыки:**
    `,play <url>` - Воспроизвести музыку по URL.
    `,stop` - Остановить воспроизведение и отключить бота.
    
    **Команды для модерации:**
    `,kick <member> <reason>` - Кикнуть пользователя с сервера.
    `,ban <member> <reason>` - Забанить пользователя.
    `,mute <member> <duration> <reason>` - Замутить пользователя на определённое время.

    **Фан Команды:**
    `,flipcoin` - Подкинуть монету (Heads/Tails).
    `,say <message>` - Бот повторяет ваше сообщение.
    `,eightball <question>` - Задайте вопрос магическому шару.
    `,randnum <min> <max>` - Сгенерировать случайное число между min и max.
    `,dadjoke` - Бот расскажет вам шутку.
    `,roll <sides>` - Бросить кубик с заданным количеством сторон.
    `,riddle` - Получить загадку.
    `,fortune` - Получить предсказание.
    `,compliment <member>` - Сделать комплимент пользователю.
    `,color` - Получить случайный цвет.

    **Примечания:**
    - Все команды начинаются с `,` (например: `,play`).
    - Некоторые команды требуют прав для их выполнения (например, `kick`, `ban`).
    """
    await ctx.send(help_text)


bot.run(TOKEN)
