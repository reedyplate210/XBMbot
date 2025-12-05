from discord.ext import commands

class Upload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def upload(self, ctx):
        """Users attach a file; bot returns a shareable playback link."""
        if not ctx.message.attachments:
            await ctx.send("❌ Please attach a file with your message.")
            return

        file = ctx.message.attachments[0]
        link = file.url
        name = file.filename

        # Simple type hints for nice message display
        if name.lower().endswith(('.mp4', '.mov', '.webm')):
            type_hint = "🎥 Video playback"
        elif name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            type_hint = "🖼️ Image preview"
        elif name.lower().endswith(('.pdf', '.txt')):
            type_hint = "📄 Read mode"
        else:
            type_hint = "📁 File link"

        await ctx.send(f"{type_hint} link for `{name}`:\n{link}")

async def setup(bot):
    await bot.add_cog(Upload(bot))
