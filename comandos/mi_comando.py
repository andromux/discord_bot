from discord.ext import commands

class Wontrix(commands.Cog):
    """Esté comando va a mandar un pdf de introducción"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="wontrix", help="Envía el manual en formato pdf")
    async def pdf_file(self, ctx):
        await ctx.send("PDF URL : https://andromux.org")

async def setup(bot):
    await bot.add_cog(Wontrix(bot))
