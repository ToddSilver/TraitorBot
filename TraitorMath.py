import random
import json


def CalculatePlayerRoles(Radio):
    with open('Config.json') as configjson:
        Config = json.load(configjson)
    maxantag = Config['Settings']['MaxAntag']
    maxtraitor = Config['Settings']['MaxTraitor']
    TraitorChance = Config['Settings']['TraitorChance']
    AntagChance = Config['Settings']['AntagChance']
    ExtraAntagifNoTraitor = Config['Settings']['ExtraAntagifNoTraitor']
    Traitor = []
    Antagonist = []
    for i in range (0, maxtraitor):
        IsTraitor = MissionChance(TraitorChance)
        if IsTraitor:
            Traitor1 = ChooseTraitor(Traitor, Radio)
            if Traitor1 != "Not enough Crew":
                Traitor.append(Traitor1)
                count = str(i)
        else:
            if ExtraAntagifNoTraitor == 1:
                print('bonus_antagonist')
                maxantag = 1+maxantag

    for i in range (0, maxantag):
        IsAntag = MissionChance(AntagChance)
        if IsAntag:
            Antagonist1 = ChooseAntagonist(Radio, Traitor, Antagonist)
            if Antagonist1 == "Not enough Crew":
                return Traitor, Antagonist
            Antagonist.append(Antagonist1)
    print(Antagonist)
    return Traitor, Antagonist

def ChooseTraitor(Traitor, Radio):
    Crew = Radio.members
    for i in Traitor:
        Crew.remove(i)
    if Crew == []:
        return "Not enough Crew"

    Traitorpick = random.randint(1, len(Crew))
    newTraitor = Crew[Traitorpick - 1]

    Traitorroles = newTraitor.roles
    for role in Traitorroles:
        if role.name == 'New':
            Traitorpick = random.randint(1, len(Crew))
            newTraitor = Crew[Traitorpick-1]

    return newTraitor

def ChooseAntagonist(Radio, Traitor, Antagonist):
    Crew = Radio.members
    for i in Traitor:
        Crew.remove(i)
    for i in Antagonist:
        Crew.remove(i)
    if Crew == []:
        return "Not enough Crew"



    Antagonist1 = Crew[random.randint(0, (len(Crew)-1))]
    return Antagonist1

def ChooseMission(Radio, player, hiddenRole):

        with open('Missions.json') as Missionjson:
            MissionFile = json.load(Missionjson)
        Missionlist=[]

        print('what the higgity heck')

        for role in player.roles:
            #if "role.name" != '@everyone' and role.name != 'New' and role.name != 'Assistant':
            try:
                Missionlist = Missionlist + MissionFile[hiddenRole][role.name]
                Missionlist = Missionlist + MissionFile[hiddenRole][role.name]
                Missionlist = Missionlist + MissionFile[hiddenRole][role.name]
                coworkers = role.members
                for i in coworkers:
                    if i not in Radio.members:
                        coworkers.remove(i)
                for x in range(1, len(coworkers)):
                    print(coworkers)
                    Missionlist = Missionlist + MissionFile[hiddenRole]['Multi']
            except KeyError:
                print('rethink this method of error catching(Keyerror for json parsing')
        Missionlist = Missionlist + MissionFile[hiddenRole]['Any']
        Missioncount = len(Missionlist)-1
        Missionpick = random.randint(0, Missioncount)
        Mission = Missionlist[Missionpick]
        #Target = ChooseTarget(Radio, Traitor1)
        return Mission

def MissionChance(Chance):
    Roll = random.randint(0, 99)
    if Roll < Chance:
        return True
    else:
        return False

def ChooseCodewords():
    list1 = ['Fishy', 'Moist', 'Damp', 'Deep', 'Sweaty', 'Lucky', 'Scaly', 'Electric', 'Umami']
    list2 = ['Crawler-Fucker', 'Pepsi-Cola', 'Dick', 'Trousers', 'Corpse', 'Fishing']
    list3 = ['Perspicacious', 'Sciatica', 'Cumulonimbus', 'Grandiloquent', 'Bäder-Meinhof', 'Confabulation']
    word1 = list1[random.randint(0, len(list1)-1)]
    word2 = list2[random.randint(0, len(list2)-1)]
    word3 = list3[random.randint(0, len(list3)-1)]
    return word1, word2, word3