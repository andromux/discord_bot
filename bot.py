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

@bot.event
async def on_ready():
    print(f"{YELLOW}✅ Bot conectado como {RESET}{GREEN}{bot.user}{RESET}")
    
    # 🎯 OPCIONES DE ESTADOS - Elige UNA de las siguientes:
    
    # 1. 🎮 JUGANDO (Playing)
    # await bot.change_presence(
    #     status=discord.Status.online,
    #     activity=discord.Game(name="ANDROMUX ORG")
    # )
    
    # 2. 🎵 ESCUCHANDO (Listening)
    # await bot.change_presence(
    #     status=discord.Status.online,
    #     activity=discord.Activity(type=discord.ActivityType.listening, name="comandos")
    # )
    
    # 3. 📺 VIENDO (Watching)
    # await bot.change_presence(
    #     status=discord.Status.online,
    #     activity=discord.Activity(type=discord.ActivityType.watching, name="el servidor")
    # )
    
    # 4. 🔴 STREAMING (Transmitiendo)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Streaming(name="ANDROMUX ORG", url="https://www.andromux.org/")
    )
    
    # 5. 🏆 COMPITIENDO (Competing)
    # await bot.change_presence(
    #     status=discord.Status.online,
    #     activity=discord.Activity(type=discord.ActivityType.competing, name="ANDROMUX")
    # )
    
    # 6. 🎨 PERSONALIZADO (Custom) - Solo funciona para usuarios, no bots
    # await bot.change_presence(
    #     status=discord.Status.online,
    #     activity=discord.CustomActivity(name="🤖 Desarrollado por ANDROMUX")
    # )
    
    print(f"{GREEN}🎯 Estado actualizado correctamente{RESET}")

# 🔄 Comando para cambiar estado dinámicamente
@bot.command(name="estado", hidden=True)
@commands.has_permissions(administrator=True)  # Solo administradores
async def cambiar_estado(ctx, tipo: str = None, *, mensaje: str = None):
    """
    Cambia el estado del bot dinámicamente
    Uso: !estado <tipo> <mensaje>
    Tipos: jugando, escuchando, viendo, streaming, compitiendo
    """
    if not tipo or not mensaje:
        embed = discord.Embed(
            title="❌ Error",
            description="Uso: `!estado <tipo> <mensaje>`\n**Tipos:** jugando, escuchando, viendo, streaming, compitiendo",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    tipo = tipo.lower()
    
    try:
        if tipo == "jugando":
            activity = discord.Game(name=mensaje)
        elif tipo == "escuchando":
            activity = discord.Activity(type=discord.ActivityType.listening, name=mensaje)
        elif tipo == "viendo":
            activity = discord.Activity(type=discord.ActivityType.watching, name=mensaje)
        elif tipo == "streaming":
            activity = discord.Streaming(name=mensaje, url="https://www.twitch.tv/andromux")
        elif tipo == "compitiendo":
            activity = discord.Activity(type=discord.ActivityType.competing, name=mensaje)
        else:
            await ctx.send("❌ Tipo no válido. Usa: jugando, escuchando, viendo, streaming, compitiendo")
            return
        
        await bot.change_presence(status=discord.Status.online, activity=activity)
        
        embed = discord.Embed(
            title="✅ Estado Cambiado",
            description=f"**Tipo:** {tipo.capitalize()}\n**Mensaje:** {mensaje}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error al cambiar estado: {e}")

# 🎲 Estados rotativos automáticos (opcional)
async def estados_rotativos():
    """Cambia el estado del bot cada ciertos minutos"""
    await bot.wait_until_ready()
    
    estados = [
        discord.Game(name="ANDROMUX ORG"),
        discord.Activity(type=discord.ActivityType.listening, name="comandos"),
        discord.Activity(type=discord.ActivityType.watching, name="el servidor"),
        discord.Streaming(name="ANDROMUX", url="https://www.andromux.org"),
        discord.Activity(type=discord.ActivityType.competing, name="con otros bots")
    ]
    
    while not bot.is_closed():
        for estado in estados:
            if bot.is_closed():
                break
            await bot.change_presence(status=discord.Status.online, activity=estado)
            await asyncio.sleep(300)  # Cambia cada 5 minutos (300 segundos)

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
        
        # 🎲 Descomenta la siguiente línea si quieres estados rotativos
        # bot.loop.create_task(estados_rotativos())
        
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
