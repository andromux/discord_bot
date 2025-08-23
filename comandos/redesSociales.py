import discord
from discord.ext import commands

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # NOTA: Los IDs de emojis personalizados (ej: <:tiktok:1275911654906789920>) 
        # son específicos del servidor de Andromux ORG. Si usas este código en otro servidor,
        # deberás reemplazar estos IDs por los emojis de tu propio servidor o usar emojis estándar.

    @commands.command(
        name="social",
        help="Muestra las redes sociales de Andromux ORG. Uso: !social"
    )
    async def social_networks(self, ctx):
        """Comando que muestra las redes sociales de Andromux ORG"""
        
        # Crear embed con información de redes sociales
        embed = discord.Embed(
            title="NO OLVIDES SEGUIRME EN MIS REDES SOCIALES",
            color=0x2F3136,  # Color oscuro similar al gray de Discord
            timestamp=discord.utils.utcnow()
        )
        
        # Establecer imagen
        embed.set_image(url="https://raw.githubusercontent.com/Retired64/Retired64/refs/heads/main/gif/social.gif")
        
        # Agregar campos de redes sociales
        # NOTA: Los emojis personalizados son específicos del servidor de Andromux ORG
        embed.add_field(
            name="<:tiktok:1275911654906789920> TikTok:",
            value="[TikTok Andromux ORG](https://www.tiktok.com/@_retired64)",
            inline=False
        )
        
        embed.add_field(
            name="<a:web:1280060230314627072> web:",
            value="[Página Web Andromux ORG](https://www.andromux.org/)",
            inline=False
        )
        
        embed.add_field(
            name="<:discord:1275911604470415443> Discord:",
            value="[Discord Andromux ORG](https://discord.com/invite/thuhUH2WNX)",
            inline=False
        )
        
        embed.add_field(
            name="<:twitter:1275911754433695856> Twitter:",
            value="[Twitter Andromux ORG](https://x.com/andromuxorg)",
            inline=False
        )
        
        embed.add_field(
            name="<:youtube:1275911490096074885> YouTube:",
            value="[YouTube Andromux ORG](https://www.youtube.com/@Andromux ORG)",
            inline=False
        )
        
        embed.add_field(
            name="<:reddit:1275911709344927839> Reddit:",
            value="[Reddit Andromux ORG](https://www.reddit.com/user/XxCmbRxX/)",
            inline=False
        )
        
        embed.add_field(
            name="<:telegram:1275911536333815964> Telegram:",
            value="[Telegram Andromux ORG](https://t.me/retired64)",
            inline=False
        )
        
        embed.add_field(
            name="<:github:1275911568558657687> GitHub:",
            value="[GitHub Retired 64](https://github.com/Andromux ORG)",
            inline=False
        )

        # Enviar el embed principal
        try:
            await ctx.send(embed=embed)
            
            # Enviar imagen adicional al final
            await ctx.send("https://raw.githubusercontent.com/andromux/andromux/refs/heads/main/.source/banner.gif")
            
        except discord.Forbidden:
            await ctx.send("⚠️ No pude enviar el embed en este canal.")
        except Exception as e:
            await ctx.send(f"❌ Error al enviar el mensaje: {str(e)}")



# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(Social(bot))
