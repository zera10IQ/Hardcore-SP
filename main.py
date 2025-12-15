import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

# Configuración inicial
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Esta función se ejecuta al inicio para cargar los Cogs
async def load_extensions():
    # Cargamos los archivos que están en la carpeta 'cogs'
    # Nota: Si creas más archivos, agrégalos a esta lista
    initial_extensions = [
        'cogs.commands',
        'cogs.events'
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'⚙️  Cog cargado: {extension}')
        except Exception as e:
            print(f'❌ Error cargando {extension}: {e}')

# Setup Hook es la forma moderna de iniciar cosas antes de que el bot corra
@bot.event
async def on_ready():
    # OJO: Es mejor no poner el sync aquí automático para no saturar la API
    print(f'✅ Logueado como {bot.user} (Main System Online)')

# Tu comando de sincronización (Mantenlo en main para control total)
@bot.command()
async def sync(ctx):
    # Reemplaza con tu ID real si quieres seguridad
    if ctx.author.id == 419746321252089866: 
        print("Sincronizando globalmente...")
        try:
            synced = await bot.tree.sync()
            await ctx.send(f"✅ ¡Listo! Se han sincronizado {len(synced)} comandos.")
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")
    else:
        await ctx.send("🔒 No tienes permiso.")

# Arranque
async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())