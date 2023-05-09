import random


def get_response(message: str) -> str:
    p_message = message.lower()
    if p_message == 'hello':
       return 'Hey there!'

    if message == 'roll':
       return str(random.randint(1,6))

    if p_message == "help":
        return "example help message"

    return 'I didn\'t understand what you wrote. Try typing "!help".'

def current_splatoon_stages():
    """
    returns a discord formatted string of the current splatoon stages
    :return: formatted str of the current splatoon stages
    """
