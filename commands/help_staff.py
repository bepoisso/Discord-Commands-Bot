'''
Filename: /opt/bot/bot_command/commands/help_staff.py
Path: /opt/bot/bot_command/commands
Created Date: Thursday, July 2nd 2026
Author: bpoisson | https://github.com/bepoisso

Copyright (c) 2026 Project Chronos
'''

"""
Command: help_staff

Displays the list of staff slash commands available on this bot.

Usage: /help_staff
Only staff with the required role can use this command.
"""
import discord
from discord import app_commands
import os
from bot_instance import bot

tree = bot.tree

staff = int(os.getenv("STAFF_ROLE")) # Staff Role

STAFF_COMMANDS = [
	("/douane_fail", "member, formulaire, raison", "Signale un échec à la douane et gère les rôles de sanction."),
	("/wl", "member, commentaire", "Whitelist un membre après réussite de la douane."),
	("/warn", "member, reason", "Envoie un avertissement à un membre."),
]

@tree.command(name="help_staff", description="Affiche la liste des commandes staff")
@app_commands.checks.has_role(staff)
async def help_staff(interaction: discord.Interaction):
	embed = discord.Embed(
		title="🛠️ Commandes Staff",
		color=discord.Color.blurple()
	)
	for name, args, desc in STAFF_COMMANDS:
		embed.add_field(name=f"{name} `{args}`", value=desc, inline=False)
	embed.set_footer(text="Chronos Bot")

	await interaction.response.send_message(embed=embed, ephemeral=True)
