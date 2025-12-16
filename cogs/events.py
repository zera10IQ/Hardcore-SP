import discord
import json
import os
from discord.ext import commands, tasks
from mcstatus import JavaServer

# Debe coincidir con el nombre de archivo en commands.py
CONFIG_FILE = "config.json"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Iniciamos el bucle apenas carga el Cog
        self.presence_loop.start()

    def cog_unload(self):
        self.presence_loop.cancel()

    # Helper para leer config
    def get_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        return None

    # --- COMANDO PARA FORZAR ACTUALIZACIÓN ---
    @commands.command(name="update")
    async def force_update(self, ctx):
        """Fuerza la actualización inmediata del estado (Rich Presence)."""
        await ctx.send("🔄 Forzando actualización de estado...")
        # .restart() cancela la espera actual y ejecuta el loop inmediatamente
        self.presence_loop.restart()

    # --- BUCLE DE ESTADO (RICH PRESENCE) ---
    @tasks.loop(seconds=30)
    async def presence_loop(self):
        config = self.get_config()
        
        # 1. Si no hay configuración
        if not config:
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="Esperando /setup"),
                status=discord.Status.idle
            )
            return

        # 2. Intentamos conectar
        try:
            address = f"{config['ip']}:{config['port']}"
            server = JavaServer.lookup(address)
            status = server.status()
            
            online = status.players.online
            max = status.players.max
            
            activity = discord.Game(name=f"Minecraft: {online}/{max} Online")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            
        except Exception:
            # 3. Si falla la conexión
            await self.bot.change_presence(
                status=discord.Status.dnd,
                activity=discord.Game(name="Servidor Offline")
            )

    @presence_loop.before_loop
    async def before_presence_loop(self):
        await self.bot.wait_until_ready()

    # --- EVENTOS ---
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'👂 Sistema de eventos listo.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        # Tu lógica anterior
        if 'sv on?' in message.content.lower():
            await message.channel.send(f'No caxo, aún no me configuran tan vio pa la wea')

    @commands.command()
    async def info(self, ctx):
        await ctx.send(f'Soy un bot de Hardcore SP :) (Versión con Auto-Update)')

async def setup(bot):
    await bot.add_cog(Events(bot))