import discord
from discord.ext import commands
import requests, os
from dotenv import load_dotenv

load_dotenv()

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *, city: str):
        """Get current weather for a city using OpenWeatherMap."""
        api_key = os.getenv("WEATHER_API_KEY")
        if not api_key:
            await ctx.send("⚠️ Weather API key not found. Please check your .env file.")
            return

        # Build API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException as e:
            await ctx.send(f"⚠️ Failed to reach the weather service: {e}")
            return

        # Handle API errors
        if response.status_code != 200:
            await ctx.send(f"❌ Could not find weather for **{city}** (status: {response.status_code})")
            return

        data = response.json()

        # Handle invalid cities
        if data.get("cod") != 200:
            msg = data.get("message", "Unknown error")
            await ctx.send(f"❌ Error: {msg.capitalize()}")
            return

        # Extract info
        name = data["name"]
        country = data["sys"].get("country", "")
        desc = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        # Create an embed for nicer display
        embed = discord.Embed(
            title=f"🌤️ Weather in {name}, {country}",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="🌡️ Temperature", value=f"{temp}°C (feels like {feels}°C)", inline=False)
        embed.add_field(name="💧 Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="🌬️ Wind", value=f"{wind} m/s", inline=True)
        embed.add_field(name="☁️ Conditions", value=desc, inline=False)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
