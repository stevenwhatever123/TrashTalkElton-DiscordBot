import discord
import time
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.voice_client import VoiceClient
from random import randrange
import datetime

# Will add a new scanner class for txt file later
#golden_words = ["Fuck you", "你都幾撚多野講", "試下收收皮", "呢度好撚迫 試下唔好講野"]

# Scanner for reading data from a text file
# Data is stored in a list and will use later for trash talking
with open('data/goldenWords.txt') as file_in:
    golden_words = [line.rstrip() for line in file_in]
    print()
    print("Words read in:")
    print(golden_words)

# Bot prefix for using command
# In this case, we use a '.'
# e.g. .command
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
# And bullshitting for a little bit
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
            save_user_id(message)
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
    await notice_someone_joined_in(member, prev, cur)
    await shut_up_when_unmuted(member, prev, cur)

# Notice all user that someone joins or leaves the voice chat
async def notice_someone_joined_in(member, prev, cur):
    if prev.channel is None and cur.channel is not None:
        # Trash talk only for Elton
        if(member.name == "Lun Yeung"):

            await member.guild.system_channel.send("撚樣已經入左黎")
        else:
            print(member.name + " joins the chat" + " (" + str(datetime.datetime.now()) + ")")
            await member.guild.system_channel.send("@" + member.name + " 個傻仔入左黎")
    else:
        print(member.name + " leaves the chat" + " (" + str(datetime.datetime.now()) + ")")
        await member.guild.system_channel.send("@" + member.name + " 個傻仔已經走左")
        
# Piss someone off when they try to mute or unmute themselves
async def shut_up_when_unmuted(member, prev, cur):
    channel = client.get_channel(384719124204355587)
    if cur.self_mute and not prev.self_mute:
        print(member.name + " stopped talking!" + " (" + str(datetime.datetime.now()) + ")")
        await channel.send("@" + member.name + " 個戇鳩已經熄撚左支咪")
    elif prev.self_mute and not cur.self_mute:
        print(member.name + " started talking!" + " (" + str(datetime.datetime.now()) + ")")
        await channel.send("@" + member.name + " 熄返個咪啦 屌你老母 冇人想聽你講野")

def save_user_id(message):
    author = message.author
    author_id = author.id
    author_name = author.name

    # Text to be printed out
    text_temp = author_name + ": " + str(author_id) + "\n"

    # See if the file we want is created before
    # If not we create one
    try:
        file = open("outputdata/" + author_name + ".txt")
    except:
        open("outputdata/" + author_name + ".txt", "a")
    
    # See if there is any content inside
    try:
        first_line_text = file.readline()
    except:
        print("There is no data")
        first_line_text = None

    # Reading the first line of the file
    # Which is the user id
    # If it has been written before
    # We ignore it
    # Otherwise, we write it in the file
    if(first_line_text == text_temp):
        file.close()
        return
    else:
        with open("outputdata/" + author_name + ".txt", "a") as text_file:
            text_file.write(text_temp)


client.run("TOKEN")