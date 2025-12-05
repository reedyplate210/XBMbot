from discord.ext import commands
import os

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = "data.txt"
        if not os.path.exists(self.file):
            open(self.file, "w").close()

    @commands.command()
    async def save(self, ctx, key: str, *, value: str):
        with open(self.file, "a", encoding="utf-8") as f:
            f.write(f"{key}:{value}\n")
        await ctx.send(f"💾 Saved `{key}`!")

    @commands.command()
    async def read(self, ctx, key: str):
        with open(self.file, "r", encoding="utf-8") as f:
            for line in f:
                k, v = line.strip().split(":", 1)
                if k == key:
                    await ctx.send(f"🔍 `{key}`: {v}")
                    return
        await ctx.send("Key not found.")

async def setup(bot):
    await bot.add_cog(Data(bot))
