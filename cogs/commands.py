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

    # --- GESTIÓN DE CONFIGURACIÓN ---
    def save_config(self, ip, port):
        data = {"ip": ip, "port": port}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return None
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    # --- COMANDO: /SV (Público) ---
    @app_commands.command(name="sv", description="Ver estado actual del servidor")
    async def sv(self, interaction: discord.Interaction):
        config = self.load_config()
        
        if not config:
            await interaction.response.send_message("❌ Bot no configurado. Un admin debe usar `/setup`.", ephemeral=True)
            return

        host = config["ip"]
        port = config["port"]
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

async def setup(bot):
    await bot.add_cog(Commands(bot))