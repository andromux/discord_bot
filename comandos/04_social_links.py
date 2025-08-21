import discord
from discord.ext import commands

class RedesSociales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="youtube", help="Muestra el canal de YouTube")
    async def youtube(self, ctx):
        embed = discord.Embed(
            title="📺 Mi Canal de YouTube",
            description="Aquí encontrarás tutoriales y contenido interesante.",
            color=discord.Color.red()
        )
        embed.add_field(name="Canal:", value="[Visítalo aquí](https://youtube.com/)", inline=False)
        embed.set_footer(text="¡No olvides suscribirte!")
        await ctx.send(embed=embed)

    @commands.command(name="twitter", help="Muestra el perfil de Twitter")
    async def twitter(self, ctx):
        embed = discord.Embed(
            title="🐦 Mi Perfil de Twitter",
            description="Sigue mis actualizaciones y noticias.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Perfil:", value="[Sígueme aquí](https://twitter.com/)", inline=False)
        embed.set_footer(text="¡Sígueme en Twitter!")
        await ctx.send(embed=embed)

    @commands.command(name="instagram", help="Muestra el perfil de Instagram")
    async def instagram(self, ctx):
        embed = discord.Embed(
            title="📸 Mi Instagram",
            description="Mira mis fotos y novedades.",
            color=discord.Color.magenta()
        )
        embed.add_field(name="Perfil:", value="[Visítalo aquí](https://instagram.com/)", inline=False)
        embed.set_footer(text="¡Dale like a mis fotos!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RedesSociales(bot))
