import discord
from discord import app_commands
from discord.ext import commands
from mcstatus import JavaServer
from utils import load_config

class UserList(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="users", description="Muestra la lista de jugadores conectados")
    async def users(self, interaction: discord.Interaction):
        # 1. Cargar configuración
        config = load_config()
        if not config:
            await interaction.response.send_message("❌ Bot no configurado. Usa `/setup`.", ephemeral=True)
            return

        host = config.get("ip")
        port = config.get("port", 25565)
        address = f"{host}:{port}"

        # 2. Avisar que estamos pensando (Query puede tardar un poco más)
        await interaction.response.defer()

        try:
            # 3. Realizar la consulta (Query)
            server = JavaServer.lookup(address)
            
            # Usamos .query()
            # Esto devuelve la lista completa real, no solo una muestra
            query = server.query()
            
            player_list = query.players.names
            count = len(player_list)

            if count == 0:
                embed = discord.Embed(
                    title="Jugadores Conectados", 
                    description="🦗 **No hay nadie jugando ahora mismo.**", 
                    color=discord.Color.yellow()
                )
            else:
                # Unimos la lista de nombres con saltos de línea
                # Si son muchos, mostramos solo los primeros 20 para no romper el embed
                if count > 20:
                    display_list = "\n".join(player_list[:20]) + f"\n...y {count-20} más."
                else:
                    display_list = "\n".join(player_list)
                
                embed = discord.Embed(
                    title=f"Jugadores Conectados ({count})", 
                    description=f"```{display_list}```", # Usamos bloque de código para que se vea limpio
                    color=discord.Color.blue()
                )

            await interaction.followup.send(embed=embed)

        except Exception as e:
            # Si falla el Query, intentar un fallback al Status normal
            try:
                status = server.status()
                embed = discord.Embed(
                    title="Jugadores (Modo Status)", 
                    description=f"Hay {status.players.online} jugadores, pero no pude obtener sus nombres completos (Revisa el puerto Query).", 
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
            except:
                await interaction.followup.send(f"⚠️ No se pudo conectar con el servidor. ¿Está online?\nError: `{e}`")

async def setup(bot: commands.Bot):
    await bot.add_cog(UserList(bot))