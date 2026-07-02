'''
Filename: /opt/bot/bot_command/main.py
Path: /opt/bot/bot_command
Created Date: Wednesday, February 4th 2026, 5:10:35 am
Author: bpoisson | https://github.com/bepoisso

Copyright (c) 2026 Project Chronos
'''

import discord
from dotenv import load_dotenv
import os
import logging
from bot_instance import bot

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL_ID   = int(os.getenv("LOG_CHANNEL"))	# Salon texte (logs)


handler = logging.FileHandler(
	filename="discord.log",
	encoding="utf-8",
	mode="w"
)

async def log(message: str):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"🛠️ **[ChronosCommande]** {message}")

@bot.event
async def on_ready():
	print(f"✅ Bot connecté : {bot.user.name}")
	await log(f"✅ Bot connecté : {bot.user.name}")

	try:
		synced = await bot.tree.sync()
		print(f"🔁 {len(synced)} slash commands synchronisées")
		await log(f"🔁 {len(synced)} slash commands synchronisées")
	except Exception as e:
		print(f"❌ Erreur sync : {e}")
		await log(f"❌ Erreur sync : {e}")

# IMPORT DES COMMANDES (OBLIGATOIRE AVANT RUN)
import commands.douane
import commands.wl
import commands.warn
# import commands.revive
# import commands.fouriere
# import commands.help_staff

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

