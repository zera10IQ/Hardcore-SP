import discord
import json
import os
from discord.ext import commands, tasks
from mcstatus import JavaServer

CONFIG_FILE = "config.json"

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.presence_loop.start()

    def cog_unload(self):
        self.presence_loop.cancel()

    def get_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return None

    @tasks.loop(seconds=30)
    async def presence_loop(self):
        config = self.get_config()
        
        if not config:
            # Si no hay config, ponemos un estado de espera
            await self.bot.change_presence(activity=discord.Game(name="Esperando /setup"))
            return

        try:
            address = f"{config['ip']}:{config['port']}"
            server = JavaServer.lookup(address)
            status = server.status()
            
            activity = discord.Game(name=f"Minecraft: {status.players.online} Jugadores")
            await self.bot.change_presence(status=discord.Status.online, activity=activity)
            
        except Exception:
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Servidor Offline"))

    @presence_loop.before_loop
    async def before_presence_loop(self):
        await self.bot.wait_until_ready()

    # ... (resto de tus eventos on_message, etc.) ...

async def setup(bot):
    await bot.add_cog(Events(bot))