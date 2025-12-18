import discord
from discord.ext import commands
# Ya no necesito el json ni load_config aquí si solo es para respuestas de chat simples

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('👂 Eventos listos.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Ejemplo simple
        if 'ip' in message.content.lower() and 'server' in message.content.lower():
            await message.channel.send('Usa `/sv` para ver la IP y el estado.')

async def setup(bot):
    await bot.add_cog(Events(bot))