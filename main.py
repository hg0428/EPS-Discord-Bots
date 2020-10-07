import discord
import nest_asyncio
import os
import time
import subprocess, shlex
nest_asyncio.apply()
import discord.utils
import random
#import threading
from discord.ext import commands
import therules
client = commands.Bot(command_prefix="!")
bad_words = ["bad-word"]
languages = eval(open("languages").read())
running = {}
os.system("pip install virtualenv")
os.system("rm -r venv\nmkdir venv")
perms = open("perms").read().split("\n")


@client.event
async def on_message(msg):
    print(msg.content, str(msg.author))
    for i in bad_words:
        if i in msg.content.lower():
            await msg.delete()
            await msg.channel.send(
                f"Sorry, @{msg.author.mention}, we found bad words in your message and had to delete it."
            )
    if msg.content.startswith("~~copy"):
        await msg.delete()
        await msg.channel.send(msg.content[6:])
    await client.process_commands(msg)


@client.command()
async def rules(ctx, num=0):
    num = int(num)
    if num == 0:
        trule = "**"
        for i in therules.rules:
            x = therules.rules[i]
            trule += f"{i}. {x}\n"
        await ctx.send(trule + "**")
    else:
        try:
            await ctx.send(therules.rules[num - 1])
        except:
            await ctx.send(
                "That is not a real rule! I am a bot, I know everything.")


@commands.has_permissions(manage_messages=True)
@client.command()
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, member: discord.Member, *, reason="Just for fun!"):
    await member.send("You have been kicked for", reason)
    await member.kick(reason=reason)


@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, member: discord.Member, reason="Just for fun!"):
    await member.send(f"You have been banned for '{reason}'.")
    await member.ban(reason=reason)


@client.command()
async def subscribe(ctx, *to):
    ctx.send("Subscibed!")
    open("sub.txt", "a")


@client.command()
async def react(ctx, num=-1, what=""):
  if ctx.message.author.mention in perms:
    a = await ctx.message.channel.history().flatten()
    await a[num].add_reaction(what)
  else:
    await ctx.send("You do not have the correct permissions.")


@client.command()
async def execute(ctx, language, code,):
    timeout=20
    if timeout!=20 and ctx.message.author.mention not in perms:
      ctx.send("You do not have permissions to change timeout. Running program with timeout 20.")

    name = str(random.random()) + str(ctx.message.author.id)
    user = ctx.message.author
    try:
        running[user].append(name)
    except:
        running[user] = [name]

    
    if code == "```":

        code = str(ctx.message.content)[str(ctx.message.content).find("\n"):-3]
    bash = f"cd venv\nvirtualenv {name}"
    os.system(bash)
    print(code)
    open("venv/" + name + "/file", "w+").write(code)
    language = languages[language]
    print(language)
    command = f"cd venv/{name}\n. bin/activate\nchmod -rwx /home/runner/\ntouch out.txt\ntimeout {timeout} {language} > out.txt\ndeactivate\nchmod +rwx /home/runner"
    os.system(command)
    output = open(f"venv/{name}/out.txt").read()
    await ctx.send(
        user.mention +
        f", your program generated the following output:\n```\n{output}\n```")
    os.system(f"cd /home/runner/EPS-Discord-Bots\nrm -r venv/{name}")
    running[user].remove(name)


@client.command()
async def addlang(ctx, name, command, time1command=""):
    if ctx.message.author.mention in perms:
        languages[name] = command.replace("\\n", "\n")
        open("languages", "w").write(languages)
        os.system(time1command)
        await ctx.send("Your lang has been added.")
    else:
        await ctx.send("You do not have the correct permissions.")


@client.command()
async def giveperm(ctx, user):
    if ctx.message.author.mention in perms:
        open("perms", "a").write(user)
    else:
        await ctx.send("You do not have the correct permissions.")


client.run(os.getenv("Key"))
