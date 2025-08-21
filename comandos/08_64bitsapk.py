import discord
from discord.ext import commands
import httpx
from urllib.parse import quote

class CoopDX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_owner_repo = "maniscat2/sm64coopdx"
        self.default_workflow = "build-coop.yaml"
        self.target_artifact = "sm64coopdx-android-arm64-x86_64.apk"  # artefacto que nos interesa

    @commands.command(
        name="coopdx",
        help="Muestra solo el APK arm64-x86_64 de maniscat2/sm64coopdx. Uso: !coopdx"
    )
    async def CoopDX(self, ctx):
        owner, repo = self.default_owner_repo.split("/")
        headers = {"Accept": "application/vnd.github+json"}

        await ctx.send(f"🔍 Buscando artefacto `{self.target_artifact}` en `{self.default_owner_repo}`...")

        # Obtener último run exitoso
        try:
            url_runs = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{self.default_workflow}/runs"
            params = {"status": "completed", "conclusion": "success", "per_page": 1}
            resp = httpx.get(url_runs, headers=headers, params=params, timeout=30.0)
            resp.raise_for_status()
            runs = resp.json().get("workflow_runs", [])
            if not runs:
                await ctx.send("⚠️ No se encontró un run exitoso.")
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

        # Filtrar solo el artefacto que nos interesa
        artifact = next((a for a in artifacts if a["name"] == self.target_artifact), None)
        if not artifact:
            await ctx.send(f"❌ Artefacto `{self.target_artifact}` no encontrado en el último run.")
            return

        # Crear embed
        size_mb = int(artifact["size_in_bytes"]) // 1024 // 1024
        safe_name = quote(artifact["name"])
        link = f"https://nightly.link/{owner}/{repo}/actions/runs/{run_id}/{safe_name}.zip"

        embed = discord.Embed(
            title=f"📦 Artefacto: {artifact['name']}",
            description=f"Tamaño: {size_mb} MB\n[Descargar APK]({link})",
            color=discord.Color.green()
        )

        # Enviar embed
        try:
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("⚠️ No pude enviar el embed en este canal.")

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(CoopDX(bot))
