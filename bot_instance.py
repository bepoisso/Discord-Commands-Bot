import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)
