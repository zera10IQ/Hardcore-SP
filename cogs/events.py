import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Este on_ready es específico de este archivo, se ejecuta junto al del main
        print(f'👂 Sistema de eventos listo.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        # Lógica personalizada
        if 'sv on?' in message.content.lower():
            await message.channel.send(f'No caxo, aún no me configuran tan vio pa la wea')
        
        # NOTA IMPORTANTE:
        # En los Cogs NO necesitas poner "await bot.process_commands(message)"
        # El bot lo hace automáticamente. Si lo pones, podrías duplicar comandos.

    @commands.command()
    async def info(self, ctx):
        await ctx.send(f'Soy un bot de Hardcore SP :) (Desde un Cog)')

async def setup(bot):
    await bot.add_cog(Events(bot))