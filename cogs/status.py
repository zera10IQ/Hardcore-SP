import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer
from utils import load_config # Importamos la herramienta de lectura

class ServerStatus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sv", description="Ver estado actual del servidor")
    async def sv(self, interaction: discord.Interaction):
        config = load_config()
        
        if not config:
            await interaction.response.send_message("❌ Bot no configurado. Un admin debe usar `/setup`.", ephemeral=True)
            return

        host = config.get("ip")
        port = config.get("port", 25565)
        address = f"{host}:{port}"

        await interaction.response.send_message("📡 Conectando...")
        mensaje = await interaction.original_response()

        try:
            server = JavaServer.lookup(address)
            status = server.status()

            embed = discord.Embed(title="Estado del Servidor", color=discord.Color.green())
            embed.add_field(name="IP", value=f"`{host}`", inline=False)
            embed.add_field(name="Jugadores", value=f"{status.players.online}/{status.players.max}", inline=True)
            embed.add_field(name="Latencia", value=f"{int(status.latency)}ms", inline=True)

            await mensaje.edit(content=None, embed=embed)

        except Exception:
            embed = discord.Embed(title="Estado del Servidor", description="🔴 **OFFLINE**", color=discord.Color.red())
            embed.add_field(name="IP", value=f"`{host}`", inline=False)
            await mensaje.edit(content=None, embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerStatus(bot))