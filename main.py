
import discord
from dotenv import load_dotenv
import os
import logging
from bot_instance import bot

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

handler = logging.FileHandler(
	filename="discord.log",
	encoding="utf-8",
	mode="w"
)



@bot.event
async def on_ready():
	print(f"✅ Bot connecté : {bot.user.name}")

	# ⚠️ À garder UNE SEULE FOIS si besoin de nettoyer Discord
	# bot.tree.clear_commands(guild=None)

	try:
		synced = await bot.tree.sync()
		print(f"🔁 {len(synced)} slash commands synchronisées")
	except Exception as e:
		print(f"❌ Erreur sync : {e}")

# IMPORT DES COMMANDES (OBLIGATOIRE AVANT RUN)
import commands.douane
import commands.wl

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

