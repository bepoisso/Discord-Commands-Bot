'''
Filename: /opt/bot/bot_command/commands/wl.py
Path: /opt/bot/bot_command/commands
Created Date: Wednesday, February 4th 2026, 5:12:01 am
Author: bpoisson | https://github.com/bepoisso

Copyright (c) 2026 Project Chronos
'''

"""
Command: wl

This Discord slash command is used by staff to whitelist a member after passing the customs (douane) process.
It automatically manages roles, sends notifications, and welcomes the member to the server.

Usage: /wl <member>
Only staff with the required role can use this command.
"""
import discord
from discord import app_commands
from datetime import datetime
import os
from bot_instance import bot

tree = bot.tree

staff = int(os.getenv("STAFF_ROLE")) # Staff Role
customs = int(os.getenv("CUSTOMS_CHANNEL")) #Channel to store message
congrat = int(os.getenv("CONGRAT_CHANNEL")) # Channel for congrat message
ff_r = int(os.getenv("FIRST_FAIL_ROLE")) # First fail role
sf_r = int(os.getenv("SECOND_FAIL_ROLE")) # Second fail role
citizen = int(os.getenv("CITIZEN_ROLE")) # Citizen Role
notCitizen = int(os.getenv("NOT_CITIZEN_ROLE")) # Not Citizen Role

@tree.command(name="wl", description="Whitliste une personne")
@app_commands.describe(
	member="Le membre à whitelist",
	commentaire="un commentaire a faire ?"
)
@app_commands.checks.has_role(staff)
async def wl(
	interaction: discord.Interaction,
	member: discord.Member,
	commentaire: str
):
	guild = interaction.guild

	channel = guild.get_channel(customs)
	congrats_channel = guild.get_channel(congrat)

	first_fail = guild.get_role(ff_r)
	second_fail = guild.get_role(sf_r)
	citoyen = guild.get_role(citizen)
	sans_papier = guild.get_role(notCitizen)

	if not all([citoyen, first_fail, second_fail, sans_papier]):
		await interaction.response.send_message(
			"Role not found. Contact @flitcher_dev",
			ephemeral=True
		)
		return

	if channel is None or congrats_channel is None:
		await interaction.response.send_message(
			"Channel not found. Contact @flitcher_dev",
			ephemeral=True
		)
		return

	await member.remove_roles(sans_papier, first_fail, second_fail)
	await member.add_roles(citoyen)

	embed = discord.Embed(
		title="💚 Whitelist réussie",
		description=(
			f"{member.mention} a réussi sa whitelist.\n\n"
			f"**Commentaire :** {commentaire}"
		),
		color=discord.Color.green(),
		timestamp=datetime.now()
	)

	embed.add_field(
		name="Nom du douanier",
		value=interaction.user.mention, inline=False
	)

	await channel.send(embed=embed)
	await congrats_channel.send(
		f"🎉 Félicitations à {member.mention} pour sa WL ! Bienvenue a toi <:s_catuwu:1462099343644299416>"
	)

	await interaction.response.send_message(
		f"Message envoyé dans <#{channel.id}>",
		ephemeral=True
	)
