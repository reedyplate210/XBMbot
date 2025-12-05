import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.load_extension("cogs.weather")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.memes")
    await bot.load_extension("cogs.data")
    await bot.load_extension("cogs.upload")  # 👈 Add this
    print("✅ All cogs loaded!")


bot.run(TOKEN)
