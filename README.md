# Discord-Commands-Bot

This is a Discord bot for managing Customs commands for GtaV RP server.

## Features
- Slash commands for whitelisting and customs (douane)
- Role management for members
- Logging to a file

## Setup
1. **Clone the repository** and place the files in `/opt/bot/bot_command`.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your environment**:
   - Create a `.env` file with your Discord bot token:
     ```env
     BOT_TOKEN=token
     ```
4. **Run the bot manually**:
   ```bash
   python3 main.py
   ```
5. **Systemd service**:
   - Make sure the user running the service has write permissions to `/opt/bot/bot_command/discord.log`.
   - Example systemd unit:
     ```ini
     [Unit]
     Description=Commands Bot
     After=network.target

     [Service]
     Type=simple
     User=bot
     Group=bot

     WorkingDirectory=/opt/bot/bot_command
     ExecStart=/usr/bin/python3 main.py

     EnvironmentFile=/opt/bot/bot_command/.env

     Restart=always
     RestartSec=5

     StandardOutput=journal
     StandardError=journal

     NoNewPrivileges=true
     PrivateTmp=true

     [Install]
     WantedBy=multi-user.target
     ```

## Folder structure
- `main.py`: Main entry point
- `bot_instance.py`: Bot instance (shared)
- `commands/`: Custom command modules
- `.env`: Environment variables
- `requirements.txt`: Python dependencies

Note: In each file inside the `commands` folder, you can modify the roles and channels using the variables defined within the file.

## Troubleshooting
- If you see `Permission denied` for `discord.log`, fix permissions with:
  ```bash
  sudo chown USER /opt/bot/bot_command
  sudo chmod u+w /opt/bot/bot_command
  ```
- Check logs in `discord.log` for errors.

## TODO
   - /revive [id]
   - /fouriere [id]
   - /warn [membre]
   - /help_staff


## Author
bpoisson [text](https://github.com/bepoisso)
