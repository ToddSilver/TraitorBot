import json


def ChangeTraitorChance(message):
    with open('Config.json') as configjson:
        Config = json.load(configjson)
    maxantag = Config['Settings']['MaxAntag']
    maxtraitor = Config['Settings']['MaxTraitor']
    TraitorChance = Config['Settings']['TraitorChance']
    AntagChance = Config['Settings']['AntagChance']

    return

def ChangeMaxTraitor(message):
    with open('Config.json') as configjson:
        Config = json.load(configjson)
    maxtraitor = message.content[15:]
    try:
        int = int(maxtraitor)
    except (ValueError, TypeError):
        return "Error - make sure your command is immediately followed by a number, i.e.: \"!SetMaxTraitors5\""
    if maxtraitor:

        return
    return