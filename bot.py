import discord
import time
import asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.voice_client import VoiceClient
from random import randrange
import datetime

# Will add a new scanner class for txt file later
#golden_words = ["Fuck you", "你都幾撚多野講", "試下收收皮", "呢度好撚迫 試下唔好講野"]


# Scanner for reading data from a text file
# Data is stored in a list and will use later for trash talking
golden_words = []
with open('data/goldenWords.txt', "r") as file_in:
    golden_words = [line.rstrip() for line in file_in]
    print()
    print("Words read in:")
    print(golden_words)

# Bot prefix for using command
# In this case, we use a '.'
# e.g. .command
client = commands.Bot(command_prefix = '.')

# Remove default help command
client.remove_command('help')

# A ready message when the bot is running
@client.event
async def on_ready():

    await client.change_presence(activity=discord.Game(name="Shisha | .help"))

    print("============")
    print("Bot is ready")
    print("============")

@client.command()
async def help(ctx):
    await ctx.send("我唔係好撚想幫你")
    await ctx.send("以下係可以用既command:")
    # Print out all commands that can be used
    helptext = "```\n"
    for command in client.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)
    await ctx.send("打 '.add_golden_words' 可以打金句入字典錄")

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
    channel = message.channel
    if(message.author == client.user):
        return
    elif(message.content.startswith(";;play")):
        print(message.author.name + " wants to listen to music" + " (" + str(datetime.datetime.now()) + ")")
        output_text = await channel.send("@" + message.author.name + " 想聽歌就自己落去聽啦")
        await asyncio.sleep(20) 
        await output_text.delete()                
        await asyncio.sleep(4) 
    elif(not message.content.startswith(".")):
        # Boolean to check if the message is one of the commands
        isCommand = False
        # Check if the input message is one of the command
        # If yes, we remind the user to add a '.' in front of it
        # Otherwise, we tell the user to shut up
        for command in client.commands:
            if(str(command) in message.content):
                isCommand = True
                print(message.author.name + " inputs a command without a '.'" + " (" + str(datetime.datetime.now()) + ")")
                output_text = await channel.send("@" + message.author.name + " 你個戇鳩試下係前面加個 '.'")
                await asyncio.sleep(20) 
                await output_text.delete()
                await asyncio.sleep(4) 
        if(not isCommand):
            save_user_id(message)
            ## Random word selection
            randnum = randrange(len(golden_words))
            string = golden_words[randnum]
            #await channel.send("Fuck you" + " (User ID:" + str(message.author.id) + ")")
            print("Just trash talked " + message.author.name + " (" + str(datetime.datetime.now()) + ")")
            output_text = await channel.send(string + " @" + message.author.name)    
            await asyncio.sleep(20) 
            await output_text.delete()
            await asyncio.sleep(4) 
    await client.process_commands(message)

# Check voice state for every memeber
@client.event
async def on_voice_state_update(member, prev, cur):
    await notice_someone_joined_and_muted(member, prev, cur)

# Notice all user that someone joins/leaves the voice chat or mute/unmute themselves
async def notice_someone_joined_and_muted(member, prev, cur):
    if prev.channel is None and cur.channel is not None:
        # Trash talk only for Elton
        if(member.name == "Elton Leo"):
            output_text = await member.guild.system_channel.send("撚樣馬頭浩宇本人已經上線了")
            await asyncio.sleep(20) 
            await output_text.delete()
            await asyncio.sleep(4) 
        else:
            # Trash talk when other memebers joins the voice channel
            print(member.name + " joins the chat" + " (" + str(datetime.datetime.now()) + ")")
            output_text = await member.guild.system_channel.send("@" + member.name + " 個傻仔入撚左黎")
            await asyncio.sleep(20) 
            await output_text.delete()
            await asyncio.sleep(4) 
    else:
        # Trash talk when someone unmute their mic
        if(prev.self_mute and not cur.self_mute):
            print(member.name + " started talking!" + " (" + str(datetime.datetime.now()) + ")")
            output_text = await member.guild.system_channel.send("@" + member.name + " 熄返個咪啦 屌你老母 冇人想聽你講野")
            await asyncio.sleep(20) 
            await output_text.delete()
            await asyncio.sleep(4) 
        else:     
            # Trash Talk when someone leaves or mute their mic      
            print(member.name + " leaves the chat/ mutes himself" + " (" + str(datetime.datetime.now()) + ")")
            output_text = await member.guild.system_channel.send("@" + member.name + " 個傻仔已經收左皮")
            await asyncio.sleep(20) 
            await output_text.delete()
            await asyncio.sleep(4) 

# Method to save user name and id
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


# Clear all bot messages that are sent before
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    channel = client.get_channel(ctx.message.channel.id)
    messages = await channel.history(limit=200).flatten()
    await ctx.send("Deleting messages")
    for message in messages:
        if(message.author.id == 743114047473451151):
            await message.delete()
    await ctx.send("Done")

# Function for reading the text file
# Parameter: file type
def read_data_file(file):
    with file as file_in:
        words_temp = [line.rstrip() for line in file_in]
        print()
        print("Words read in:")
        print(words_temp)
    return words_temp


# command for recieveing suggestions to golden words text file from other users
@client.command()
async def add_golden_words(ctx, message):
    global golden_words
    text = message + "\n"
    try:
        file = open("data/goldenWords.txt", "a+")
    except:
        open("data/goldenWords.txt", "a+")
    print("Golden words added by " + ctx.message.author.name + " (" + str(datetime.datetime.now()) + ")")
    result_text = "```\n"
    result_text += text
    result_text += "```"
    await ctx.send(result_text + " 已經入左金句錄")
    file.write(text)
    file.flush()
    file.seek(0)
    golden_words = read_data_file(file)

# Command for printing all elements in our golden words list
@client.command()
async def print_golden_words(ctx):
    await ctx.send("馬頭浩宇金句錄包括：")
    # Print out all golden words in the txt file
    global golden_words
    helptext = "```\n"
    for words in golden_words:
        helptext+=f"{words}\n"
    helptext+="```"
    await ctx.send(helptext)

# Command for deleting a specific element in our golden words list
@client.command()
async def del_golden_words(ctx, message):
    global golden_words
    text = message
    try:
        file = open("data/goldenWords.txt", "r+")
    except:
        open("data/goldenWords.txt", "r+")
    # Boolean on whether the message is part of our list
    words_found = False
    with open("data/goldenWords.txt", "r") as f:
        lines = f.readlines()
    with open("data/goldenWords.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != text:
                f.write(line)
            else:
                words_found = True            
    if(words_found is True):
        await ctx.send("已經del左 " + "'" + text + "'")
    else:
        await ctx.send("我既金句字典冇呢句")
    # Update Golden Words list   
    golden_words = read_data_file(file)

client.run("TOKEN")