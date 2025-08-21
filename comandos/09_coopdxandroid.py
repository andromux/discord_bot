import discord
from discord.ext import commands
import httpx
from urllib.parse import quote

class CoopDXAndroid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Valores predeterminados
        self.default_owner_repo = "maniscat2/sm64coopdx"
        self.default_workflow = "build-coop.yaml"

    @commands.command(
        name="coopdxandroid",
        help="Muestra los últimos artefactos del workflow build-coop.yaml de maniscat2/sm64coopdx. Uso: !coopdxandroid"
    )
    async def coopdxandroid(self, ctx):
        owner_repo = self.default_owner_repo
        workflow = self.default_workflow
        owner, repo = owner_repo.split("/")
        headers = {"Accept": "application/vnd.github+json"}

        await ctx.send(f"🔍 Obteniendo últimos artefactos de `{owner_repo}`...")

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

        # Preparar mensaje con los enlaces
        mensaje = f"📦 **Artefactos del último run ({run_id}) de `{owner_repo}`**\n\n"
        for art in artifacts:
            name = art["name"]
            size_mb = int(art["size_in_bytes"]) // 1024 // 1024
            safe_name = quote(name)
            link = f"https://nightly.link/{owner}/{repo}/actions/runs/{run_id}/{safe_name}.zip"
            mensaje += f"**{name}** ({size_mb} MB)\n{link}\n\n"

        # Link general al run
        mensaje += f"🌐 [Todos los artefactos](https://nightly.link/{owner}/{repo}/actions/runs/{run_id})"

        # Enviar mensaje en el canal
        try:
            if len(mensaje) > 2000:
                bloques = [mensaje[i:i+1990] for i in range(0, len(mensaje), 1990)]
                for bloque in bloques:
                    await ctx.send(f"```{bloque}```")
            else:
                await ctx.send(mensaje)
        except discord.Forbidden:
            await ctx.send(f"⚠️ No pude enviar los artefactos en este canal.")

# ----------- Setup -----------
async def setup(bot):
    await bot.add_cog(CoopDXAndroid(bot))
