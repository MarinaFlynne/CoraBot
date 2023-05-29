from io import BytesIO

import responses
import discord
from discord import app_commands
from discord.ext import commands
import Splatoon.Splatoon as splat

TOKEN = "MTEwMjM2MzIwOTcwMjMyNjM4Mg.GiBXht.1Ya9KFlS9lNiGu2dOjoaXc7X6UOJ4jRnLEJQXA"


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
        pass
    except Exception as e:
        print(e)


def run_discord_bot():
    # intents = discord.Intents.default()
    # intents.message_content = True
    # client = discord.Client(intents=intents)
    # tree = app_commands.CommandTree(client) # defines the command tree
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print("Bot is up and ready!")
        try:
            synced = await bot.tree.sync(guild=discord.Object(id=705499607102259230))
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name="stages", guild=discord.Object(id=705499607102259230))
    async def stages(interaction: discord.Interaction):
        stages = responses.get_stages_embed()
        image = splat.main()
        # image = image.resize((200, 200))
        # image.show()
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        # # Create a File object from the PIL image bytes
        file = discord.File(image_bytes, filename="image.png")
        stages.set_image(url="attachment://image.png")

        await interaction.response.send_message(file=file, embed=stages)

    # test command
    @bot.tree.command(name="test", guild=discord.Object(id=705499607102259230))
    async def test(interaction: discord.Interaction):
        stages = responses.get_stages_embed()
        image = splat.main()
        image = image.resize((200, 200))
        # image.show()
        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        # # Create a File object from the PIL image bytes
        file = discord.File(image_bytes, filename="image.png")
        stages.set_image(url="attachment://image.png")

        await interaction.response.send_message(file=file, embed=stages)

    bot.run(TOKEN)

    # @client.event
    # async def on_ready():
    #     await tree.sync(guild=discord.Object(id=705499607102259230))
    #     print(f'{client.user} is now running')
    #
    # @client.event
    # async def on_message(message):
    #     if message.author == client.user:
    #         return
    #
    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
    #
    #     print(f"{username} said: \"{user_message}\" ({channel})")
    #
    #     if user_message[0] == '?':
    #         user_message = user_message[1:]
    #         await send_message(message, user_message, is_private=True)
    #     else:
    #         await send_message(message, user_message, is_private=False)
    #
    # client.run(TOKEN)

# # hello command
#     @bot.tree.command(name="hello", guild=discord.Object(id=705499607102259230))
#     async def hello(interaction: discord.Interaction):
#         stages = splat.get_cur_regular_stages()
#         message = f'{stages[0]}\n{stages[1]}'
#         await interaction.response.send_message(message, ephemeral=False)
#
#     # say command
#     @bot.tree.command(name="say", guild=discord.Object(id=705499607102259230))
#     @app_commands.describe(arg="What should I say?")
#     async def say(interaction: discord.Interaction, arg: str):
#         await interaction.response.send_message(f"{interaction.user.name} said: '{arg}'")
#
#     # gamestop price command
#     @bot.tree.command(name="gamestop", guild=discord.Object(id=705499607102259230))
#     @app_commands.describe(game="Enter a game name")
#     async def say(interaction: discord.Interaction, game: str):
#         await interaction.response.send_message(f"{interaction.user.name} said: '{game}'")
