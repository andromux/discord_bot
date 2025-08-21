import discord
from discord.ext import commands

class Ayuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ayuda", help="Muestra este mensaje de ayuda")
    async def ayuda(self, ctx):
        embed = discord.Embed(
            title="📖 Menú de Ayuda",
            description="Lista de comandos disponibles en el bot",
            color=discord.Color.purple()
        )

        # Recorremos todos los comandos del bot
        for comando in self.bot.commands:
            if comando.hidden:  # Ignora comandos ocultos
                continue
            embed.add_field(
                name=f"❯ {ctx.prefix}{comando.name}",
                value=comando.help or "Sin descripción",
                inline=False
            )

        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ayuda(bot))

