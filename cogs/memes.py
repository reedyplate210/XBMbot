import discord
from discord.ext import commands
import random, requests

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 🧠 You can edit this list any time
        self.subreddits = [
            "memes",
            "dankmemes",
            "Darkmemes4u"
        ]

    @commands.command()
    async def meme(self, ctx):
        """Fetch a random meme from Reddit (custom subreddits)."""
        subreddit = random.choice(self.subreddits)
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
        headers = {"User-Agent": "XBMbot/1.0 (by u/yourredditusername)"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            await ctx.send(f"⚠️ Couldn’t fetch memes: `{e}`")
            return

        posts = [
            post["data"] for post in data["data"]["children"]
            if not post["data"]["stickied"]
            and post["data"].get("url_overridden_by_dest", "").endswith((".jpg", ".png", ".gif"))
        ]

        if not posts:
            await ctx.send("❌ No suitable memes found right now. Try again later.")
            return

        post = random.choice(posts)
        title = post["title"]
        image_url = post["url_overridden_by_dest"]
        permalink = f"https://reddit.com{post['permalink']}"
        upvotes = post.get("ups", 0)
        subreddit_name = post["subreddit"]

        embed = discord.Embed(
            title=f"😂 {title}",
            url=permalink,
            color=discord.Color.random()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=f"👍 {upvotes} upvotes | r/{subreddit_name}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Memes(bot))
