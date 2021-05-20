import json


def ChangeTraitorChance(message):
    with open('Config.json') as configjson:
        Config = json.load(configjson)
    maxantag = Config['Settings']['MaxAntag']
    newmaxtraitor = Config['Settings']['MaxTraitor']
    TraitorChance = Config['Settings']['TraitorChance']
    AntagChance = Config['Settings']['AntagChance']

    traitorchance = message.content[17:]
    try:
        newtraitorchance = int(traitorchance)
    except (ValueError, TypeError):
        return "Error - make sure your command is immediately followed by a number, i.e.: \"!SetTraitorChance5\""
    configjson = open('Config.json', 'r')
    Config = json.load(configjson)

    Config['Settings']['MaxTraitor'] = newmaxtraitor
    TraitorChance = str(Config['Settings']['TraitorChance'])
    print(Config['Settings']['MaxTraitor'])
    configjson = open('Config.json', 'w')
    configjson.write(json.dumps(Config))
    return ("There will now be a "+TraitorChance+" chance per roll of up to "+maxtraitor+" traitors.")

def ChangeMaxTraitor(message):
    maxtraitor = message.content[15:]
    try:
        newmaxtraitor = int(maxtraitor)
    except (ValueError, TypeError):
        return "Error - make sure your command is immediately followed by a number, i.e.: \"!SetMaxTraitors5\""
    configjson = open('Config.json', 'r')
    Config = json.load(configjson)

    Config['Settings']['MaxTraitor'] = newmaxtraitor
    TraitorChance = str(Config['Settings']['TraitorChance'])
    print(Config['Settings']['MaxTraitor'])
    configjson = open('Config.json', 'w')
    configjson.write(json.dumps(Config))
    return ("There will now be a "+TraitorChance+" chance per roll of up to "+maxtraitor+" traitors.")

def ViewSetting(message):

    return

def ChangeSetting(message):
    return

def ResetSetting(message):
    return