from io import BytesIO
import responses
import discord
from discord import app_commands
from discord.ext import commands
import Splatoon.Splatoon as Splat

CONFIG = "config.txt"


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
        pass
    except Exception as e:
        print(e)


def read_config() -> dict:
    """
    reads the config file and returns a dict containing all the config settings
    :return: dictionary containing all the config settings
    """
    config_dict = {}
    # open and get lines from config file
    with open(CONFIG) as config:
        lines = config.readlines()
    # read through each line and save key + value to the dict
    for line in lines:
        if line[0] != "#":  # commented lines will start with #, so we do not want to read them
            key, value = line.strip().split("=")
            config_dict[key.strip()] = value.strip()
    return config_dict


def run_discord_bot():
    config: dict = read_config()
    if config['token'] == "" or config['token'] == "12345":
        print("Invalid bot token. Please set your token in 'config.txt'")

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


    @bot.event
    async def on_ready():
        print("Bot is up and ready!")
        try:
            # check if the config file has the guild_id set.
            # The guild ID determines which discord server the bot will work on.
            # Mostly for testing purposes. Slash commands take a while to update if you don't set a guild ID.
            if "guild_id" in config and ("guild_id" != "12345" or "guild_id" != ""):
                synced = await bot.tree.sync(guild=discord.Object(id=config["guild_id"]))
            else:
                synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name="stages", guild=discord.Object(id=config["guild_id"]))
    async def stages(interaction: discord.Interaction):
        stages = responses.get_stages_embed()
        image = Splat.main() # TODO fix
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        # Create a File object from the PIL image bytes
        file = discord.File(image_bytes, filename="image.png")
        stages.set_image(url="attachment://image.png")

        await interaction.response.send_message(file=file, embed=stages)

    bot.run(config['token'])
