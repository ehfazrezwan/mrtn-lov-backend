import base64
import discord
from discord.ext import commands
from io import BytesIO

from core.config import settings

TOKEN = settings.DISCORD_BOT_TOKEN


class DiscordClient:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = commands.Bot(command_prefix="!", intents=intents)

    async def on_ready(self):
        print("Juniper is ready!")

    async def share_image(
        self,
        base64_image_string: str,
        text_prompt: str,
        channel_id: int = settings.DISCORD_IMG_CHANNEL_ID,
    ):
        channel = self.client.get_channel(channel_id)
        img_data = base64.b64decode(base64_image_string)

        image_file = discord.File(BytesIO(img_data), filename="image.png")
        await channel.send(f"**Prompt**: {text_prompt}\n\n", file=image_file)

    async def log_error(self, error_message: str, channel_id: int):
        channel = self.client.get_channel(channel_id)

        # Format the error message as a code block with Python syntax highlighting
        formatted_error_message = f"```python\n**Error**: {error_message}\n```"

        await channel.send(formatted_error_message)

    async def start(self):
        self.client.add_listener(self.on_ready)
        await self.client.start(TOKEN)

    async def close(self):
        await self.client.close()
