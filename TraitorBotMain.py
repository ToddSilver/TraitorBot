import discord
import random
import json
import time
import asyncio
import TraitorMath
import TraitorConfigs

client = discord.Client()
@client.event

async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
#async def on_reaction_add(reaction, user):
    #if bot.is_owner(user) and str(reaction.emoji) == "👎":
        #VARIABLE = False

@client.event
async def on_message(message):
    if message.author == client.user:
        return
   # elif message.content.startswith('!client'):
    #    From dotenv import load_dotenv
    #    load_dotenv()
  #      token - 
    #    return
    elif message.content.startswith('!help'):
        await message.channel.send('Currently available commands: \n!gamestart - Assigns 0, 1 or more traitors and '
                                   'antagonists from all players in your voicechannel based on game settings. '
                                   '\n!gamestop - clears current traitor(s).\n!SetTraitorChance50 - replace 50 with '
                                   'any number (0-100) for a percent chance of traitor this round. \n!role - Opens '
                                   'the role assignment chat.  React to the message to choose a role.\n!clearrole - '
                                   'removes your in-game roles, including "New"\n!reroll - If you are Traitor, '
                                   'or Antagonist, and need a new mission, this command will randomly pick a new one. '
                                   ' Should be used in the Traitor/Antag channel to avoid giving yourself away.  '
                                   'Please do not overuse this command, there are not many missions at this point.')
        return
    elif message.content.startswith('!SetTraitorChance'):
        traitorchance = message.content[17:]
        #if traitorchance is integer 2 or 3 digits
        #with open('Config.json') as configfile:
            #MissionFile = json.load(configfile)
        #
        
        return
    elif message.content.startswith('!SetMaxTraitors'):
        print(TraitorConfigs.ChangeMaxTraitor(message))
        return
    elif message.content.startswith('!SetMaxAntags'):
        maxantag = message.content[13:]
        return        
        
    elif message.content.startswith('!role'):
        Bserver = message.guild
        message1 = await message.channel.send('React to this message in the next 30 seconds to set your role:')
        # \nDoctor :morphine: \n Security :baton: \n Captain :cap:\nEngineer :Screwdriver:\nMechanic :wrench~1:\nAssistant :Ethanol:
        with open('Config.json') as configjson:
            Config = json.load(configjson)
        settingsroles = Config['Settings']['AvailableRoles']
        emojis = []
        for rolename in settingsroles:
            emoji1 = discord.utils.get(Bserver.emojis, name=rolename)
            emojis.append(emoji1)
            await message.channel.send(rolename + ' = ' + (str(emoji1)))
        for emoji in emojis:
            await message1.add_reaction(emoji)
            #await message.channel.send(str(emoji))
        
        def check(reaction, user):
            return user != client.user
        #Run for 30 seconds and then break.
        stoptime = time.time() + 30
        print(stoptime)
        print(time.time())
        while stoptime>time.time():
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=35.0, check=check)
            except asyncio.TimeoutError:
                print('Write this timeout part better')    
            else:
                for role in settingsroles:
                    oldRole = discord.utils.get(message.guild.roles, name=role)
                    await user.remove_roles(oldRole)
                role = reaction.emoji.name
                newRole = discord.utils.get(message.guild.roles, name=role)
                await user.add_roles(newRole)
                await message.channel.send('Role changed for ' + user.name)

        await message.channel.send('Done changing roles.')



    elif message.content.startswith('!gamestart'):
        try:
            Radio = message.author.voice.channel
        except AttributeError:
            await message.channel.send('Error: You (and other players) must be in the same voice channel to start the game.')
        if len(Radio.members) < 2:
            await message.channel.send('Error: Looks like there are not enough players.  At least 2 players must be present in the voice channel.')
            #return
        await message.channel.send('Welcome to the game!  Now distributing insanity')
        Bserver = message.guild
        Traitor, Antagonist = TraitorMath.CalculatePlayerRoles(Radio)
        word1, word2, word3 = TraitorMath.ChooseCodewords()
        setCodewordsTraitors = False
        setCodewordsAntag = False
        setCodeCount = 0
        with open('Config.json') as configjson:
            Config = json.load(configjson)
        CodewordChance = Config['Settings']['CodewordChance']
        if (len(Traitor) >= 2):
            Roll = random.randint(0, 99)
            if Roll < CodewordChance:
                setCodewordsTraitors = True
        if (len(Traitor) >= 1) and (len(Antagonist) >= 1) and not setCodewordsTraitors:
            Roll = random.randint(0, 99)
            if Roll < CodewordChance:
                setCodewordsTraitors = True
                setCodewordsAntag = True
        for index, player in enumerate(Traitor, start=1):
            index = str(index)
            Traitorcoms = await Bserver.create_text_channel('traitor-' + index)
            await Traitorcoms.set_permissions(Bserver.default_role, read_messages=False, send_messages=False)
            await Traitorcoms.set_permissions(player, read_messages=True, send_messages=True)
            await Traitorcoms.send('You have developed Deep Sea Madness, {}'.format(player.mention))
            if setCodewordsTraitors and setCodeCount < 2:
                Mission = TraitorMath.ChooseMission(Radio, player, 'CodewordsTraitor')
                await Traitorcoms.send(Mission)
                await Traitorcoms.send(word1 + '\n' + word2 + '\n' + word3)
                setCodeCount = setCodeCount+1
            else:
                Mission = TraitorMath.ChooseMission(Radio, player, 'TraitorMissions')
                await Traitorcoms.send(Mission)

        for index, player in enumerate(Antagonist, start=1):
            index = str(index)
            Antagcoms = await Bserver.create_text_channel('antag-' + index)
            await Antagcoms.set_permissions(Bserver.default_role, read_messages=False, send_messages=False)
            await Antagcoms.send('You have developed a minor case of Deep Sea Madness, {}'.format(player.mention))
            await Antagcoms.set_permissions(player, read_messages=True, send_messages=True)
            if setCodewordsAntag and setCodeCount < 2:
                Mission = TraitorMath.ChooseMission(Radio, player, 'CodewordsAntag')
                await Antagcoms.send(Mission)
                await Antagcoms.send(word1 + '\n' + word2 + '\n' + word3)
                setCodeCount = setCodeCount+1
            else:
                Mission = TraitorMath.ChooseMission(Radio, player, 'AntagMissions')
                await Antagcoms.send(Mission)

        if setCodewordsAntag or setCodewordsTraitors:
            Roll = random.randint(0, 99)
            if Roll < 33:
                crew = Radio.members
                for i in Traitor:
                    crew.remove(i)
                for i in Antagonist:
                    crew.remove(i)
                if crew == []:
                    spy = 'Not enough Crew'
                else:
                    spy = crew[random.randint(0, (len(crew)-1))]
                if (spy != 'Not enough Crew'):
                    Spycoms = Bserver.create_text_channel('spy-' + '1')
                    Spycoms.set_permissions(Bserver.default_role, read_messages=False, send_messages=False)
                    Spycoms.set_permissions(spy, read_messages=True, send_messages=True)
                    Spycoms.send('You have received a report that there are at least two traitors on board that will be trying to identify eachother with codewords.  Below is one of the words they will be using.  Make sure they face justice for their crimes but you CANNOT reveal your information or identity as a spy to the other crew.')
                    Spycoms.send('Codeword = ' + word2)
      
    elif message.content.startswith('!gamestop'):
        Bserver = message.guild
        rascals = []
        for channel in Bserver.text_channels:
            if ("antag" in channel.name) or ("traitor" in channel.name) or ("spy" in channel.name):
                for traitor in channel.members:
                    rascals.append(traitor.name)
                await channel.delete()


        await message.channel.send('All hidden roles removed. It looks like these were the crew with special missions.  What a bunch of rascals')
        for i in rascals:
            if (i != 'TraitorBot'):
                await message.channel.send(i + ' was not a nice sailor')

        return

    elif message.content.startswith('!reroll'): 
        Bserver = message.guild
        Radio = message.author.voice.channel
        Traitorcoms = discord.utils.get(Bserver.text_channels, name="traitor-1")
        Antagcoms = discord.utils.get(Bserver.text_channels, name="antag-1")
        Channel = message.channel
        if Channel == Traitorcoms:
            Mission = TraitorMath.ChooseMission(Radio, message.author, 'TraitorMissions')
            #Target = TraitorMath.ChooseTarget(Radio, message.author)
            await Traitorcoms.send(Mission)
        elif Channel == Antagcoms:
            Mission = TraitorMath.ChooseMission(Radio, message.author, 'AntagMissions')
            await Antagcoms.send(Mission)
        else:
            await Channel.send('Sorry it broke tell Todd \n Error code:didnt finish this part #12')
            return
    else:
        if message.content.startswith('!'):
            await message.channel.send('Unknown Command.  Type !help for commands.')

def BotMessage(m):
    return m.author == client.user


client.run('NzA2OTg0NTE0NTY3NjY3ODMy.XrCMow.ZIc5SyfUL2ZrIG7SLXi9p28xOgA')