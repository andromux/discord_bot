import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Cargamos las variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Intents necesarios (para que el bot pueda leer mensajes)
intents = discord.Intents.default()
intents.message_content = True

# Creamos el bot con prefijo "!"
bot = commands.Bot(command_prefix="!", intents=intents)

# Evento: cuando el bot esté listo
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ----------- COMANDOS CON DECORADORES -----------

# 1. Comando de saludo
@bot.command(name="saludo", help="El bot te saluda con un mensaje personalizado")
async def saludo(ctx):
    await ctx.send(f"👋 ¡Hola {ctx.author.mention}! Bienvenido al servidor.")

# 2. Comando con un Embed y una URL
@bot.command(name="info", help="Muestra un embed con información y un link")
async def info(ctx):
    embed = discord.Embed(
        title="Información del Bot 🤖",
        description="Este es un bot de prueba hecho con **discord.py**",
        color=discord.Color.blue()
    )
    embed.add_field(name="Comandos", value="`!saludo` y `!info`", inline=False)
    embed.add_field(name="Enlace útil", value="[Visita Python](https://www.python.org)", inline=False)
    embed.set_footer(text="Bot creado por MekkeL el Crack")
    
    await ctx.send(embed=embed)

# -------------------------------------------------

# Iniciamos el bot
bot.run(TOKEN)
