import discord
from discord.ext import commands
import json
import os
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

async def setup(bot):
    await bot.add_cog(Events(bot))