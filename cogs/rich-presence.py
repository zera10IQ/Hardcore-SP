import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer

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