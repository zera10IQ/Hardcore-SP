import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer

# --- COMANDO: /SETUP (Solo Admin) ---
@app_commands.command(name="setup", description="Configura la IP del servidor de Minecraft")
@app_commands.describe(ip="IP o Dominio (ej. hardcoresp.duckdns.org)", port="Puerto (default 25565)")
@commands.has_permissions(administrator=True)
async def setup(self, interaction: discord.Interaction, ip: str, port: int = 25565):
    try:
        # Validamos conexión antes de guardar
        address = f"{ip}:{port}"
        await interaction.response.defer(thinking=True)
        
        server = JavaServer.lookup(address)
        latency = server.ping() # Si falla, salta al except
        
        self.save_config(ip, port)
        
        embed = discord.Embed(title="✅ Configuración Guardada", color=discord.Color.green())
        embed.add_field(name="Dirección", value=f"`{address}`")
        embed.add_field(name="Estado", value=f"Conectado ({int(latency)}ms)")
        
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        await interaction.followup.send(f"⚠️ No se pudo conectar a `{ip}:{port}`.\nError: {e}")