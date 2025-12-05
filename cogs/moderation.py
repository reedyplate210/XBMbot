import discord
from discord.ext import commands
import re
from datetime import timedelta, datetime, timezone

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- KICK COMMAND ---
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} was kicked. Reason: {reason or 'None'}")

    # --- BAN COMMAND ---
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} was banned. Reason: {reason or 'None'}")

    # --- PURGE COMMAND ---
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Delete the specified number of recent messages."""
        if amount <= 0:
            await ctx.send("⚠️ Please specify a positive number of messages to delete.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.", delete_after=5)

    # --- ALERT COMMAND ---
    @commands.command()
    @commands.has_permissions(mention_everyone=True)
    async def alert(self, ctx, *, message: str):
        """Ping @everyone with an alert message."""
        await ctx.send(f"🚨 **ALERT:** @everyone\n{message}")

    # --- TICKET COMMAND ---
    @commands.group(invoke_without_command=True)
    async def ticket(self, ctx, *, reason: str = "No reason provided"):
        """Create a private help ticket channel for user support."""
        guild = ctx.guild
        category_name = "🎫 Tickets"

        category = discord.utils.get(guild.categories, name=category_name)
        if category is None:
            category = await guild.create_category(category_name)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True)

        channel_name = f"ticket-{ctx.author.name}".replace(" ", "-").lower()
        existing = discord.utils.get(category.channels, name=channel_name)
        if existing:
            await ctx.send(f"📨 You already have an open ticket: {existing.mention}")
            return

        ticket_channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            topic=f"Support ticket opened by {ctx.author} | Reason: {reason}",
        )

        await ticket_channel.send(
            f"🎫 Ticket created by {ctx.author.mention}\nReason: **{reason}**\nAn admin will assist you soon.\n\nTo close this ticket, type `!ticket close`."
        )
        try:
            await ctx.author.send(f"✅ Your ticket has been created: {ticket_channel.mention}")
        except discord.Forbidden:
            await ctx.send(f"✅ Your ticket has been created: {ticket_channel.mention}\n*(I couldn’t DM you, please check your privacy settings)*")


    @ticket.command(name="close")
    async def close_ticket(self, ctx):
        """Close (delete) the current ticket channel."""
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ This command can only be used inside a ticket channel.")
            return

        from datetime import datetime, timedelta, timezone

        await ctx.send("🗑️ Closing this ticket in 5 seconds...")
        close_time = datetime.now(timezone.utc) + timedelta(seconds=5)
        await discord.utils.sleep_until(close_time)
        await ctx.channel.delete(reason=f"Ticket closed by {ctx.author}")


    # --- TIMEOUT COMMAND ---
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason="No reason provided"):
        """
        Timeout a user for a specified duration.
        Format example: !timeout @user 1d2h3m4s
        """

        # Parse duration string
        time_regex = re.compile(r"((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?")
        parts = time_regex.fullmatch(duration)
        if not parts:
            await ctx.send("❌ Invalid time format! Example: `!timeout @user 1d2h3m4s`")
            return

        time_params = {name: int(value) for name, value in parts.groupdict(default=0).items()}
        delta = timedelta(**time_params)

        if delta.total_seconds() <= 0:
            await ctx.send("⚠️ Duration must be greater than 0.")
            return

        until = datetime.now(timezone.utc) + delta
        try:
            await member.timeout(until, reason=reason)
            await ctx.send(f"⏳ {member.mention} has been timed out for **{duration}**. Reason: {reason}")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to timeout that user.")
        except Exception as e:
            await ctx.send(f"⚠️ Something went wrong: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
