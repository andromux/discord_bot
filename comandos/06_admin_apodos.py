import discord
from discord.ext import commands

class AdminApodo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="apodo", 
        help="(Solo administradores) Cambia el apodo de un usuario. Uso: !apodo @usuario NuevoNombre"
    )
    @commands.has_permissions(administrator=True)  # 👈 Solo admins pueden usarlo
    async def apodo(self, ctx, miembro: discord.Member, *, nuevo_apodo: str):
        try:
            # Cambiar el apodo
            await miembro.edit(nick=nuevo_apodo)
            await ctx.send(f"✅ El apodo de {miembro.mention} ha sido cambiado a **{nuevo_apodo}**")
        except discord.Forbidden:
            await ctx.send("⚠️ No tengo permisos para cambiar el apodo de ese usuario.")
        except Exception as e:
            await ctx.send(f"❌ Ocurrió un error: {e}")

    # Si alguien intenta usarlo sin permisos
    @apodo.error
    async def apodo_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 No tienes permisos para usar este comando. Solo administradores pueden hacerlo.")

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(AdminApodo(bot))
