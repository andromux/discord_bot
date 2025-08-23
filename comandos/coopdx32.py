import discord
from discord.ext import commands
import httpx
from urllib.parse import quote

class Releases(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Valores predeterminados
        self.default_owner_repo = "Sploder-Saptarshi/sm64coopdx-android"
        self.default_workflow = "build-coop.yaml"

    @commands.command(
        name="splod32",
        help="Muestra solo el artefacto 'sm64coopdx arm apk' de la acción build-coop.yaml. Uso: !splod32"
    )
    async def splot32(self, ctx):
        owner_repo = self.default_owner_repo
        workflow = self.default_workflow
        owner, repo = owner_repo.split("/")
        headers = {"Accept": "application/vnd.github+json"}

        await ctx.send(f"🔍 Obteniendo artefacto 'sm64coopdx arm apk' de `{owner_repo}`...")

        # Obtener el último run exitoso
        try:
            url_runs = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow}/runs"
            params = {"status": "completed", "conclusion": "success", "per_page": 1}
            resp = httpx.get(url_runs, headers=headers, params=params, timeout=30.0)
            resp.raise_for_status()
            runs = resp.json().get("workflow_runs", [])
            if not runs:
                await ctx.send("⚠️ No se encontró un run exitoso para este workflow.")
                return
            run_id = runs[0]["id"]
        except Exception as e:
            await ctx.send(f"❌ Error al obtener el último run: {str(e)}")
            return

        # Obtener artefactos
        try:
            url_artifacts = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
            resp = httpx.get(url_artifacts, headers=headers, timeout=30.0)
            resp.raise_for_status()
            artifacts = resp.json().get("artifacts", [])
            if not artifacts:
                await ctx.send("⚠️ No hay artefactos disponibles en este run.")
                return
        except Exception as e:
            await ctx.send(f"❌ Error al obtener artefactos: {str(e)}")
            return

        # Filtrar solo el artefacto específico
        target_artifact = None
        for art in artifacts:
            if art["name"] == "sm64coopdx arm apk":
                target_artifact = art
                break

        if not target_artifact:
            await ctx.send("⚠️ No se encontró el artefacto 'sm64coopdx arm apk' en este run.")
            return

        # Crear embed solo para el artefacto específico
        embed = discord.Embed(
            title=f"📦 {target_artifact['name']}",
            description=f"Repositorio: `{owner_repo}` | Run: {run_id}",
            color=discord.Color.green()
        )

        name = target_artifact["name"]
        size_mb = int(target_artifact["size_in_bytes"]) // 1024 // 1024
        safe_name = quote(name)
        link = f"https://nightly.link/{owner}/{repo}/actions/runs/{run_id}/{safe_name}.zip"
        
        embed.add_field(
            name=f"📱 Tamaño: {size_mb} MB", 
            value=f"[📥 Descargar APK]({link})", 
            inline=False
        )

        # Link general al run (opcional)
        embed.add_field(
            name="🌐 Ver todos los artefactos", 
            value=f"[Abrir en Nightly]({f'https://nightly.link/{owner}/{repo}/actions/runs/{run_id}'})", 
            inline=False
        )

        # Enviar embed
        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(f"⚠️ No pude enviar el artefacto en este canal.")

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(Releases(bot))
