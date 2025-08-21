import discord
from discord.ext import commands

class Saludo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="saludo", help="El bot te saluda con un mensaje personalizado")
    async def saludo(self, ctx):
        await ctx.send(f"👋 ¡Hola {ctx.author.mention}! Bienvenido al servidor.")

async def setup(bot):
    await bot.add_cog(Saludo(bot))
