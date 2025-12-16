import discord
import json
import os
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer

CONFIG_FILE = "config.json"

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Función auxiliar para guardar configuración
    def save_config(self, ip, port):
        data = {"ip": ip, "port": port}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    # Función auxiliar para leer configuración
    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return None
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    # --- COMANDO DE CONFIGURACIÓN ---
    @app_commands.command(name="setup", description="Configura la IP del servidor de Minecraft")
    @app_commands.describe(ip="La IP o dominio del servidor", port="El puerto (default 25565)")
    @commands.has_permissions(administrator=True) # Solo admins pueden usarlo
    async def setup(self, interaction: discord.Interaction, ip: str, port: int = 25565):
        try:
            # Probamos si la IP es válida antes de guardar
            address = f"{ip}:{port}"
            await interaction.response.defer(thinking=True) # Damos tiempo para verificar
            
            server = JavaServer.lookup(address)
            latency = server.ping() # Si esto falla, saltará al except
            
            self.save_config(ip, port)
            
            embed = discord.Embed(title="✅ Configuración Guardada", color=discord.Color.green())
            embed.add_field(name="IP Establecida", value=f"`{ip}`")
            embed.add_field(name="Puerto", value=f"`{port}`")
            embed.add_field(name="Estado", value=f"Conectado (Ping: {int(latency)}ms)")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(f"⚠️ No se pudo conectar a `{ip}:{port}`. Verifica los datos.\nError: {e}")

    # --- COMANDO DE ESTADO (/sv) ---
    @app_commands.command(name="sv", description="Ver estado del servidor de Minecraft")
    async def sv(self, interaction: discord.Interaction):
        config = self.load_config()
        
        if not config:
            await interaction.response.send_message("❌ El bot no está configurado. Usa `/setup` primero.", ephemeral=True)
            return

        host = config["ip"]
        port = config["port"]
        address = f"{host}:{port}"

        await interaction.response.send_message("📡 Conectando...")
        mensaje = await interaction.original_response()

        try:
            server = JavaServer.lookup(address)
            status = server.status()

            embed = discord.Embed(
                title="Estado del Servidor",
                description="✅ **ONLINE**",
                color=discord.Color.green()
            )
            embed.add_field(name="IP", value=f"`{host}`", inline=False)
            embed.add_field(name="Jugadores", value=f"{status.players.online}/{status.players.max}", inline=True)
            embed.add_field(name="Ping", value=f"{int(status.latency)}ms", inline=True)

            await mensaje.edit(content=None, embed=embed)

        except Exception:
            embed = discord.Embed(
                title="Estado del Servidor",
                description="❌ **OFFLINE**",
                color=discord.Color.red()
            )
            embed.add_field(name="IP", value=f"`{host}`", inline=False)
            await mensaje.edit(content=None, embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))