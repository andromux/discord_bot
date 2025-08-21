import discord
from discord.ext import commands

class Emuladores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Diccionario con la info de cada emulador
        self.emuladores = {
            "citra": {
                "titulo": "🎮 Emulador Citra",
                "descripcion": "Citra es un emulador de Nintendo 3DS para PC y dispositivos móviles.",
                "imagen": "https://raw.githubusercontent.com/citra-emu/citra-web/master/public/citra-logo.png",
                "url": "https://citra-emu.org/download/"
            },
            "dolphin": {
                "titulo": "🎮 Emulador Dolphin",
                "descripcion": "Dolphin es un emulador de Nintendo GameCube y Wii para PC.",
                "imagen": "https://dolphin-emu.org/images/logo.png",
                "url": "https://dolphin-emu.org/download/"
            },
            "eden": {
                "titulo": "🎮 Emulador Eden",
                "descripcion": "Eden es un emulador experimental de consolas retro.",
                "imagen": "https://example.com/eden-logo.png",
                "url": "https://example.com/eden-download"
            }
        }

    @commands.command(
        name="emulador",
        help="Muestra información de un emulador. Uso: !emulador <nombre> o !emulador"
    )
    async def emulador(self, ctx, nombre: str = None):
        if nombre is None:
            # Mostrar mini menú con todos los emuladores
            embed = discord.Embed(
                title="🎮 Lista de Emuladores Disponibles",
                description="Usa `!emulador <nombre>` para ver información detallada.",
                color=discord.Color.orange()
            )
            for key, info in self.emuladores.items():
                embed.add_field(
                    name=info["titulo"],
                    value=f"{info['descripcion']}\n[Descarga aquí]({info['url']})",
                    inline=False
                )
            await ctx.send(embed=embed)
            return

        # Si se proporcionó nombre del emulador
        nombre = nombre.lower()
        if nombre not in self.emuladores:
            disponibles = ", ".join(self.emuladores.keys())
            await ctx.send(f"❌ Emulador no encontrado. Nombres disponibles: {disponibles}")
            return

        info = self.emuladores[nombre]

        embed = discord.Embed(
            title=info["titulo"],
            description=info["descripcion"],
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=info["imagen"])
        embed.add_field(name="Descarga oficial", value=f"[Clic aquí]({info['url']})", inline=False)
        await ctx.send(embed=embed)

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(Emuladores(bot))