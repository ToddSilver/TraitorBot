import json



def ViewSetting():
    configjson = open('Config.json', 'r')
    Config = json.load(configjson)
    doctext = ""
    for docLine in Config['Documentation']:
        doctext = doctext + '\n\n*' + docLine + '* = ' + str(Config['Settings'][docLine]) + '.  ' + Config['Documentation'][docLine]
        #Look into using join here instead
    return doctext

def ChangeSetting(message):

    settingindex = (message.find('_')+1)
    valueindex = (message.find('_', settingindex)+1)
    setting = message[settingindex:valueindex-1]
    print(setting)
    newvalue = message[valueindex:]
    print(newvalue)
    try:
        inttest = int(newvalue)
    except (ValueError, TypeError):
        return "Error - make sure your command is in the following format:\"!ChangeSetting_MaxTraitor_3\""
    configjson = open('Config.json', 'r')
    Config = json.load(configjson)
    try:
        oldvalue = str(Config['Settings'][setting])
    except (KeyError, TypeError):
        return "Error - I can't find the setting you are trying to edit. Did you mess up the format? Try: \"!ChangeSetting_MaxTraitor_3\""
    Config['Settings'][setting] = newvalue
    configjson = open('Config.json', 'w')
    configjson.write(json.dumps(Config))

    return (setting + " has been updated from " +oldvalue+ " to " + newvalue)

def ResetSetting(message):
    return