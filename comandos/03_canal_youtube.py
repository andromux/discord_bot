import discord
from discord.ext import commands

class CanalYouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="canal", help="Muestra el canal de YouTube recomendado")
    async def canal(self, ctx):
        await ctx.send("📺 Visita mi canal de YouTube: https://youtube.com/")

async def setup(bot):
    await bot.add_cog(CanalYouTube(bot))

