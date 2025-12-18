import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer
from utils import save_config

class Setup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # --- COMANDO: /SETUP (Solo Admin) ---
    @app_commands.command(name="setup", description="Configura la IP del servidor de Minecraft")
    @app_commands.describe(ip="IP o Dominio (ej. miserver.com)", port="Puerto (default 25565)")
    @commands.has_permissions(administrator=True)
    async def setup_command(self, interaction: discord.Interaction, ip: str, port: int = 25565):
        # Diferimos la respuesta porque comprobar la conexión puede tardar
        await interaction.response.defer(thinking=True)
        
        address = f"{ip}:{port}"
        
        try:
            # 1. Valida conexión antes de guardar
            server = JavaServer.lookup(address)
            latency = server.ping() 
            
            # 2. Si la conexión fue exitosa, guardamos usando utils.py
            if save_config(ip, port):
                embed = discord.Embed(title="✅ Configuración Guardada", color=discord.Color.green())
                embed.add_field(name="Dirección", value=f"`{address}`", inline=False)
                embed.add_field(name="Estado", value=f"Conectado ({int(latency)}ms)", inline=False)
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send("⚠️ Error interno al guardar el archivo de configuración.")

        except Exception as e:
            await interaction.followup.send(f"⚠️ No se pudo conectar a `{address}`. Verifica la IP.\nError: `{e}`")

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))