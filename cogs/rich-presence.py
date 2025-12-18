import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
from utils import load_config

class RichPresence(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Iniciamos el bucle al cargar el Cog
        self.presence_loop.start()

    def cog_unload(self):
        self.presence_loop.cancel()

    @tasks.loop(seconds=30)
    async def presence_loop(self):
        config = load_config()
        
        # Si no hay config, mostramos estado de espera
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

async def setup(bot: commands.Bot):
    await bot.add_cog(RichPresence(bot))