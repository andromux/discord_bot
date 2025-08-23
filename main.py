import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

# 🎨 Códigos ANSI para colores
CYAN = "\033[96m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuración de intents
intents = discord.Intents.default()
intents.message_content = True

# Crear bot con prefijo y desactivar help por defecto
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Evento cuando el bot está listo

# Actualmente hay 5 estados
# en Discord y son:
# Listening, Streaming,
# Listening, Custom
# Competing.

@bot.event
async def on_ready():
    # custom = discord.Custom('Prueba')
    # await bot.change_presence(status=discord.Status.online, activity=custom)
    print(f"{YELLOW}✅ Bot conectado como {RESET}{GREEN}{bot.user}{RESET}")

# ----------- AUTO-CARGA DE COMANDOS (Cogs) -----------
async def cargar_comandos():
    for archivo in os.listdir("./comandos"):
        if archivo.endswith(".py") and not archivo.startswith("__"):
            await bot.load_extension(f"comandos.{archivo[:-3]}")
            print(f"{CYAN}📥 Cargado:{RESET} {BLUE}{archivo}{RESET}")

# ----------- FUNCIÓN PRINCIPAL -----------
async def main():
    async with bot:
        await cargar_comandos()
        try:
            await bot.start(TOKEN)
        except asyncio.CancelledError:
            print("🛑 Bot detenido con CTRL + C")
            await bot.close()
        except KeyboardInterrupt:
            print("🛑 Bot interrumpido manualmente (KeyboardInterrupt)")
            await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot terminado desde consola")
