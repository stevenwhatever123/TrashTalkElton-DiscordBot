import discord
import time
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from random import randrange
import datetime

# Will add a new scanner class for txt file later
golden_words = ["Fuck you", "你都幾撚多野講", "試下收收皮", "呢度好撚迫 試下唔好講野"]

client = commands.Bot(command_prefix = '.')

# A ready message when the bot is running
@client.event
async def on_ready():
    print("==============")
    print("Bot is ready")
    print("==============")

# Trash Talk text
@client.command()
async def comecome(ctx):
    await ctx.send("Lets trash talk")

# Elton so funny
@client.command()
async def youSoFunny(ctx):
    await ctx.send("She smokes shisha in the seashore")

#家康式係呀
@client.command()
async def samwong33(ctx):
    time.sleep(5)
    await ctx.send("係呀")

# Command not found handler
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        print(ctx.message.author.name + " inputs a wrong command" + " (" + str(datetime.datetime.now()) + ")")
        await ctx.send("指令都唔撚識 洗唔洗驗下個腦")
        await ctx.send("可以用既command:")
        # Print out all commands that can be used
        helptext = "```\n"
        for command in client.commands:
            helptext+=f"{command}\n"
        helptext+="```"
        await ctx.send(helptext)
        return
    raise error

# BM someone whenever someone texted
@client.event
async def on_message(message):
    if(message.author == client.user):
        return
    elif(not message.content.startswith(".")):
        # Boolean to check if the message is one of the commands
        isCommand = False
        channel = message.channel
        # Check if the input message is one of the command
        # If yes, we remind the user to add a '.' in front of it
        # Otherwise, we tell the user to shut up
        for command in client.commands:
            if(str(command) in message.content):
                isCommand = True
                print(message.author.name + " inputs a command without a '.'" + " (" + str(datetime.datetime.now()) + ")")
                await channel.send("@" + message.author.name + " 你個戇鳩試下係前面加個 '.'")
        if(not isCommand):
            ## Random word selection
            randnum = randrange(len(golden_words))
            string = golden_words[randnum]
            #await channel.send("Fuck you" + " (User ID:" + str(message.author.id) + ")")
            print("Just trash talked " + message.author.name + " (" + str(datetime.datetime.now()) + ")")
            await channel.send(string + " @" + message.author.name)     
    await client.process_commands(message)

# Check voice state for every memeber
@client.event
async def on_voice_state_update(member, prev, cur):
    await shut_up_when_unmuted(member, prev, cur)

# Piss someone off when they try to mute or unmute their microphone
async def shut_up_when_unmuted(member, prev, cur):
    channel = client.get_channel(384719124204355587)
    if cur.self_mute and not prev.self_mute:
        print(member.name + " stopped talking!" + " (" + str(datetime.datetime.now()) + ")")
        await channel.send("@" + member.name + " 個戇鳩已經熄撚左支咪")
    elif prev.self_mute and not cur.self_mute:
        print(member.name + " started talking!" + " (" + str(datetime.datetime.now()) + ")")
        await channel.send("@" + member.name + " 熄返個咪啦 屌你老母 冇人想聽你講野")

client.run("TOKEN")