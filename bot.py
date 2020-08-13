import discord
import time
from discord.ext import commands
from random import randrange

# Will add a new scanner class for txt file later
golden_words = ["Fuck you", "你都幾撚多野講", "試下收收皮", "呢度好撚迫 試下唔好講野"]

client = commands.Bot(command_prefix = '.')

# A ready message when the bot is running
@client.event
async def on_ready():
    print("Bot is ready")

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

# BM someone whenever someone texted
@client.event
async def on_message(message):
    if(message.author == client.user):
        return
    elif(not message.content.startswith(".")):
        channel = message.channel
        ## Random word selection
        randnum = randrange(len(golden_words))
        string = golden_words[randnum]
        #await channel.send("Fuck you" + " (User ID:" + str(message.author.id) + ")")
        await channel.send(string + " @" + message.author.name)
    await client.process_commands(message)

# Check voice state for every memeber
@client.event
async def on_voice_state_update(member, prev, cur):
    await shut_up_when_unmuted(member, prev, cur)

# Method to tell someone to shut up
async def shut_up_when_unmuted(member, prev, cur):
    channel = client.get_channel(384719124204355587)
    if cur.self_mute and not prev.self_mute:
        print(member.name + " stopped talking!")
        await channel.send("@" + member.name + " 個戇鳩已經熄撚左支咪")
    elif prev.self_mute and not cur.self_mute:
        print(member.name + " started talking!")
        await channel.send("@" + member.name + " 熄返個咪啦 屌你老母 冇人想聽你講野")

client.run("Token")