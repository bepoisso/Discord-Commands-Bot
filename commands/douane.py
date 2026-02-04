'''
Filename: /opt/bot/bot_command/commands/douane.py
Path: /opt/bot/bot_command/commands
Created Date: Wednesday, February 4th 2026, 5:12:12 am
Author: bpoisson | https://github.com/bepoisso

Copyright (c) 2026 Project Chronos
'''

"""
Command: douane_fail

This Discord slash command is used by staff to mark a member as having failed the customs (douane) process.
It automatically manages roles for first, second, and definitive failures, sends notifications, and ensures proper sanctions.

Usage: /douane_fail <member> <form number>
Only staff with the required role can use this command.
"""
import discord
from discord import app_commands
from datetime import datetime, timedelta
from bot_instance import bot

tree = bot.tree

staff = 1462145081803800666 #Staff Role
customs = 1468304263292915836 #Channel to store message
ff_r = 1468429857292550320 # First fail role
sf_r = 1468448474625343529 # Second fail role
df_r = 1468449578792784053 # Definitiv fail role

@tree.command(name="douane_fail", description="Une personne a echouee la douane")
@app_commands.describe(
	member="Le membre à sanctionner",
	formulaire="Numéro du formulaire (1, 2 ou 3)"
)
@app_commands.checks.has_role(staff)
async def douane_fail(
	interaction: discord.Interaction,
	member: discord.Member,
	formulaire: int
):
	guild = interaction.guild

	channel = guild.get_channel(customs)

	first_fail = guild.get_role(ff_r)
	second_fail = guild.get_role(sf_r)
	definitive_fail = guild.get_role(df_r)

	if not all([first_fail, second_fail, definitive_fail]):
		await interaction.response.send_message(
			"Role not found. Contact @flitcher_dev",
			ephemeral=True
		)
		return

	if channel is None:
		await interaction.response.send_message(
			"Channel not found. Contact @flitcher_dev",
			ephemeral=True
		)
		return

	if formulaire not in (1, 2, 3):
		await interaction.response.send_message(
			"Mauvais numero de formulaire",
			ephemeral=True
		)
		return

	if second_fail in member.roles:
		count = 3
		repassage_days = 0
		await member.remove_roles(second_fail)
		await member.add_roles(definitive_fail)

	elif first_fail in member.roles:
		count = 2
		repassage_days = 2
		await member.remove_roles(first_fail)
		await member.add_roles(second_fail)

	else:
		count = 1
		repassage_days = 1
		await member.add_roles(first_fail)

	now = datetime.now()
	repassage_date = (now + timedelta(days=repassage_days)).strftime("%d/%m/%Y %H:%M")

	if count == 1:
		title = "🚫 Douane échouée"
		color = discord.Color.orange()
	elif count == 2:
		title = "🚫 Douane échouée une seconde fois"
		color = discord.Color.red()
	else:
		title = "🚫 Douane échouée DEFINITIVEMENT"
		color = discord.Color.dark_red()

	embed = discord.Embed(
		title=title,
		description=f"{member.mention}",
		color=color,
		timestamp=now
	)

	embed.add_field(name="Nom du douanier", value=interaction.user.mention)
	embed.add_field(name="Numéro de formulaire", value=str(formulaire))

	if count in (1, 2):
		embed.add_field(name="Date de repassage", value=repassage_date)

	embed.set_footer(text="Chronos Bot")

	await channel.send(embed=embed)
	await interaction.response.send_message(
		f"Message envoyé dans <#{channel.id}>",
		ephemeral=True
	)
