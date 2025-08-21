import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", help="Muestra un embed con información y un link")
    async def info(self, ctx):
        embed = discord.Embed(
            title="Información del Bot 🤖",
            description="Este es un bot modular con **Cogs**",
            color=discord.Color.blue()
        )
        embed.add_field(name="Comandos", value="`!saludo`, `!info`, `!canal`", inline=False)
        embed.add_field(name="Enlace útil", value="[Visita Python](https://www.python.org)", inline=False)
        embed.set_footer(text="Bot creado por MekkeL el Crack")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))