import discord
import json
import os
from discord.ext import commands, tasks
from mcstatus import JavaServer

# Personalidad y Rich Presence

CONFIG_FILE = "config.json"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_loop.start()

    def cog_unload(self):
        self.presence_loop.cancel()

    def get_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    # --- EVENTOS DE TEXTO (CHAT) ---
    @commands.Cog.listener()
    async def on_message(self, message):
        # Evitar que el bot se responda a sí mismo
        if message.author == self.bot.user:
            return

        msg = message.content.lower()

        # Ejemplo 1: Pregunta por el estado
        if 'se cayó el server?' in msg:
            await message.channel.send('Usa /sv para ver si estoy ON :)')

    # --- EVENTOS DE SISTEMA ---
    @commands.Cog.listener()
    async def on_ready(self):
        print('👂 Módulo de Eventos y Respuestas listo.')

    # --- BUCLE RICH PRESENCE (Automático) ---
    @tasks.loop(seconds=30)
    async def presence_loop(self):
        config = self.get_config()
        
        if not config:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Esperando /setup"))
            return

        try:
            address = f"{config['ip']}:{config['port']}"
            server = JavaServer.lookup(address)
            status = server.status()
            
            activity = discord.Game(name=f"Minecraft: {status.players.online}/{status.players.max} Online")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
        except:
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Servidor Offline"))

    @presence_loop.before_loop
    async def before_presence_loop(self):
        await self.bot.wait_until_ready()
    
    # --- COMANDO EXTRA (Utilidad para eventos) ---
    @commands.command(name="update")
    async def force_update(self, ctx):
        """Fuerza la actualización del estado del bot inmediatamente."""
        await ctx.send("🔄 Actualizando estado...")
        self.presence_loop.restart()

async def setup(bot):
    await bot.add_cog(Events(bot))