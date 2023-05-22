import random
import discord
import Splatoon.Splatoon as splat

def get_response(message: str) -> str:
    p_message = message.lower()
    if p_message == 'hello':
       return 'Hey there!'

    if message == 'roll':
       return str(random.randint(1,6))

    if p_message == "help":
        return "example help message"

    return 'I didn\'t understand what you wrote. Try typing "!help".'

def get_stages_embed():
    """
    returns an embed current splatoon stages
    :return: embed of the current splatoon stages
    """
    stages = splat.get_cur_regular_stages()
    start_time = stages[0].start_time
    end_time = stages[0].end_time
    embed = discord.Embed(
        title='Current Regular Battle Stages',
        description=f'<t:{start_time}:t> - <t:{end_time}:t>',
        color=discord.Color.blue()
    )
    embed.add_field(name=stages[0].name, value='', inline=False)
    embed.add_field(name=stages[1].name, value='', inline=False)
    embed.set_image(url=stages[0].img)
    embed.set_thumbnail(url='https://www.seekpng.com/png/detail/41-416602_splatoon-turf-war-symbol.png')

    return embed

