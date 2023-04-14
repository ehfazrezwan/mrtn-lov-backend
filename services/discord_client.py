import discord
from discord.ext import commands
import base64
from io import BytesIO


class DiscordClient(discord.Client):
    def __init__(self, command_prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        print("Bot is ready")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!hello"):
            await message.channel.send("Hello!")

    async def send_image(self, img_base64: str, prompt: str, channel_id: int):
        channel = self.get_channel(channel_id)

        image_data = base64.b64decode(img_base64)
        image_file = BytesIO(image_data)
        image_file.name = "image.png"

        discord_file = discord.File(image_file, filename="image.png")

        await channel.send(f"**Prompt**: {prompt}", file=discord_file)

    async def send_error(self, error: str, channel_id: int):
        channel = self.get_channel(channel_id)

        embed = discord.Embed(
            title="Error",
            description=f"**Error**: ```python\n{error}```",
            color=0xFF0000,
        )
        embed.add_field(name="Error", value=error, inline=False)

        await channel.send(embed)

    async def run_bot(self, token):
        try:
            await self.start(token)
        except KeyboardInterrupt:
            await self.logout()
            await self.close()
