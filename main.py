import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('token')

# Configuración inicial
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True         
bot = commands.Bot(command_prefix='!', intents=intents)

# Función para cargar extensiones
async def load_extensions():
    # Lista actualizada de archivos en la carpeta cogs
    initial_extensions = [
        'cogs.setup',          # Para configurar la IP
        'cogs.status',         # El comando /sv
        'cogs.rich-presence',  # Estado del bot (Jugando a...)
        'cogs.events'          # Eventos de chat
        # 'cogs.user-list'     # Descomentar cuando termine el archivo
    ]
    
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'⚙️  Cog cargado: {extension}')
        except Exception as e:
            print(f'❌ Error cargando {extension}: {e}')

@bot.event
async def on_ready():
    print(f'✅ Logueado como {bot.user} (Main System Online)')
    # Sincronizamos los comandos slash al iniciar
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"⚠️ Error sincronizando comandos: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())