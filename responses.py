import random
from io import BytesIO

import discord
import Splatoon.Splatoon as Splat

def get_response(message: str) -> str:
    p_message = message.lower()
    if p_message == 'hello':
       return 'Hey there!'

    if message == 'roll':
       return str(random.randint(1,6))

    if p_message == "help":
        return "example help message"

    return 'I didn\'t understand what you wrote. Try typing "!help".'

def get_stages_embed(type) -> tuple:
    """
    returns an embed current splatoon stages
    :return: file containing the image to display and embed of the current splatoon stages
    """
    stages = Splat.get_cur_stages(type) # TODO CHANGE TO DICT
    mode = stages[2]
    thumbnail = stages[3]
    title = stages[4]

    start_time = stages[0].start_time
    end_time = stages[0].end_time

    embed = discord.Embed(
        title= f'Current {title} Stages',
        description=f'Mode: **{mode}**\n<t:{start_time}:t> - <t:{end_time}:t>',
        color=discord.Color.blue()
    )
    embed.add_field(name=f'{stages[0].name} - {stages[1].name}', value='', inline=False)

    embed.set_thumbnail(url=thumbnail)

    img1 = stages[0].img
    img2 = stages[1].img
    image = Splat.merge_images(img1, img2)

    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    # Create a File object from the PIL image bytes
    file = discord.File(image_bytes, filename="image.png")
    embed.set_image(url="attachment://image.png")

    return file, embed

