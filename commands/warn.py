'''
Filename: /opt/bot/bot_command/commands/warn.py
Path: /opt/bot/bot_command/commands
Created Date: Wednesday, February 4th 2026, 6:46:25 pm
Author: bpoisson | https://github.com/bepoisso

Copyright (c) 2026 Project Chronos
'''

"""
Warn command for Discord bot to sanction a member with a warning.

This command allows staff members to issue a warning to a specified member, providing a reason for the warning.
An embed message is sent to a designated warning channel, containing details about the warned member, the staff member issuing the warning, and the reason.

Args:
	interaction (discord.Interaction): The interaction object representing the command invocation.
	member (discord.Member): The member to be warned.
	reason (str): The reason for the warning.

Raises:
	app_commands.errors.MissingRole: If the user invoking the command does not have the required staff role.

Note:
	Only users with the staff role can use this command.

# This function sends a warning embed to a specific channel and notifies the staff member that the action was successful.
"""

import discord
from discord import app_commands
from datetime import datetime, timedelta
import os
from bot_instance import bot

tree = bot.tree

staff = int(os.getenv("STAFF_ROLE")) #Staff Role
warn_c = int(os.getenv("WARN_CHANNEL")) # Warn Channel

@tree.command(name="warn", description="Sanctioner un joueur d'un warn")
@app_commands.describe(
	member="Le membre à sanctionner",
	reason="La Raison du warn"
)
@app_commands.checks.has_role(staff)
async def warn(
	interaction: discord.Interaction,
	member: discord.Member,
	reason: str
):
	guild = interaction.guild
	channel = guild.get_channel(warn_c)
	now = datetime.now()
	title = "⚠️ WARN ⚠️"
	color = discord.Color.red()
	embed = discord.Embed(
		title=title,
		description=f"{member.mention} a reçu un warn",
		color=color,
		timestamp=now
	)

	embed.add_field(name="Nom du staff", value=interaction.user.mention, inline=False)
	embed.add_field(name="Raison", value=str(reason), inline=False)
	embed.set_footer(text="Chronos Bot")

	await interaction.response.defer(ephemeral=True)

	try:
		await channel.send(embed=embed)

		dm_embed = discord.Embed(
			title="⚠️ Vous avez reçu un avertissement ⚠️",
			description=f"{member.mention}, Vous avez recu un warn",
			color=discord.Color.red(),
			timestamp=now
		)
		dm_embed.add_field(name="Staff", value=interaction.user.mention, inline=False)
		dm_embed.add_field(name="Raison", value=str(reason) + "\n\nPour contester cette décision, ouvrez un ticket.", inline=False)
		dm_embed.set_footer(text="Chronos Bot")
		await member.send(embed=dm_embed)

		await interaction.followup.send(
			f"Message envoyé dans <#{channel.id}> et le joueur a été prévenu de la sanction.",
			ephemeral=True
		)
	except discord.Forbidden:
		await interaction.followup.send(
			f"Message envoyé dans <#{channel.id}>, mais le joueur n'a pas pu être prévenu en privé.",
			ephemeral=True
		)
	except Exception as e:
		await interaction.followup.send(
			f"Une erreur s'est produite : {e}\n Contacter Flitcher_dev",
			ephemeral=True
		)
