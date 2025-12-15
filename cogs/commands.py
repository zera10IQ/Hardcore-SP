import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer

# Variables de configuración
HOST_DNS = "hardcoresp.duckdns.org"
PORT = 25565

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sv", description="Ver estado del servidor de Minecraft")
    async def sv(self, interaction: discord.Interaction):
        await interaction.response.send_message("📡 Conectando con la base...")
        mensaje = await interaction.original_response()
        direccion_completa = f"{HOST_DNS}:{PORT}"

        try:
            server = JavaServer.lookup(direccion_completa)
            status = server.status()

            embed = discord.Embed(
                title="Estado del Servidor",
                description="✅ **ONLINE**",
                color=discord.Color.green()
            )
            embed.add_field(name="IP para entrar", value=f"`{HOST_DNS}`", inline=False)
            embed.add_field(name="Jugadores", value=f"{status.players.online}/{status.players.max}", inline=True)
            embed.add_field(name="Ping", value=f"{int(status.latency)}ms", inline=True)

            await mensaje.edit(content=None, embed=embed)

        except Exception as e:
            print(f"Error de conexión: {e}")
            
            embed = discord.Embed(
                title="Estado del Servidor",
                description="❌ **OFFLINE**",
                color=discord.Color.red()
            )
            embed.add_field(name="Host", value=f"`{HOST_DNS}`", inline=False)
            embed.add_field(name="Posible causa", value="El PC está apagado o el puerto cerrado.", inline=False)
            
            await mensaje.edit(content=None, embed=embed)

# Función de setup obligatoria para cargar el Cog
async def setup(bot):
    await bot.add_cog(Commands(bot))