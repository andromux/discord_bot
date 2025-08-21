import discord
from discord.ext import commands
from discord.ui import View, Button

class Roms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roms = {
            "ps2": {
                "final fantasy x": "https://example.com/ffx-download",
                "shadow of the colossus": "https://example.com/sotc-download",
                "god of war ii": "https://example.com/gow2-download",
                "metal gear solid 3": "https://example.com/mgs3-download",
                "devil may cry 3": "https://example.com/dmc3-download"
            },
            "3ds": {
                "pokemon omega ruby": "https://example.com/pokemon-or-download",
                "super mario 3d land": "https://example.com/sm3dl-download",
                "zelda ocarina of time 3d": "https://example.com/zelda3d-download",
                "fire emblem awakening": "https://example.com/fe-download",
                "mario kart 7": "https://example.com/mk7-download"
            }
        }
        self.items_por_pagina = 3

    @commands.command(
        name="roms",
        help="Muestra juegos de una consola o un juego específico. Uso: !roms <consola> [nombre_del_juego]"
    )
    async def roms(self, ctx, consola: str, *, juego: str = None):
        consola = consola.lower()
        if consola not in self.roms:
            disponibles = ", ".join(self.roms.keys())
            await ctx.author.send(f"❌ Consola no encontrada. Consolas disponibles: {disponibles}")
            return

        juegos_consola = self.roms[consola]

        if juego:
            juego = juego.lower()
            juegos_consola = {nombre: url for nombre, url in juegos_consola.items() if juego in nombre}
            if not juegos_consola:
                await ctx.author.send(f"❌ Juego no encontrado en {consola.upper()}.")
                return

        lista_juegos = list(juegos_consola.items())
        total_paginas = (len(lista_juegos) - 1) // self.items_por_pagina + 1

        def crear_embed(pagina):
            embed = discord.Embed(
                title=f"🎮 Juegos {consola.upper()} (Página {pagina+1}/{total_paginas})",
                color=discord.Color.orange()
            )
            start = pagina * self.items_por_pagina
            end = start + self.items_por_pagina
            for nombre, url in lista_juegos[start:end]:
                embed.add_field(name=nombre.title(), value=f"[Descarga aquí]({url})", inline=False)
            return embed

        # View privada para el usuario
        class Paginador(View):
            def __init__(self):
                super().__init__()
                self.pagina = 0

            @discord.ui.button(label="⬅️", style=discord.ButtonStyle.blurple)
            async def anterior(self, interaction: discord.Interaction, button: Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("❌ Solo puedes manipular tu propia lista.", ephemeral=True)
                    return
                if self.pagina > 0:
                    self.pagina -= 1
                    await interaction.response.edit_message(embed=crear_embed(self.pagina), view=self)

            @discord.ui.button(label="➡️", style=discord.ButtonStyle.blurple)
            async def siguiente(self, interaction: discord.Interaction, button: Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("❌ Solo puedes manipular tu propia lista.", ephemeral=True)
                    return
                if self.pagina < total_paginas - 1:
                    self.pagina += 1
                    await interaction.response.edit_message(embed=crear_embed(self.pagina), view=self)

        # Enviar primer embed **como DM al usuario**
        try:
            await ctx.author.send(embed=crear_embed(0), view=Paginador())
            if ctx.guild:  # opcional: avisar en el canal que el mensaje se envió por DM
                await ctx.send(f"📥 {ctx.author.mention}, te he enviado la lista de ROMs por DM.")
        except discord.Forbidden:
            await ctx.send(f"⚠️ {ctx.author.mention}, no pude enviarte un DM. Revisa tu configuración de privacidad.")

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(Roms(bot))
