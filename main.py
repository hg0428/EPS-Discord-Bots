def fix(f="main.py"):
    a = open(f).read()
    open(f, "w").write(a.replace(" " * 2, "\t"))


#fix()
import asyncio
import re
from typing import Union
from os import getenv
import discord
import time
import helps
import tools
import discord.ext.commands as commands

m = tools.m
import threading

client = m.client
uses = {}
banned = {}


def setInterval():
    def wrapper(funct):
        def repeat(*args, **kwargs):
            return funct(*args, **kwargs)

        threading.Timer(5, funct).start()
        return repeat

    return wrapper


#https://discordpy.readthedocs.io/en/latest/api.html#event-reference
#https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#ext-commands-api-errors
def CLEAN(text):
    text = text.lower()
    return "".join([
        i for i in text if i in ''.join(list(map(chr, range(97, 123)))) + " "
    ])


client.remove_command('help')
'''
@client.event
async def on_command(ctx):
    print("Executed:", ctx.command)
    if ctx.message.author.id in uses:
      uses[ctx.message.author.id].append(time.time())
    else:
      uses[ctx.message.author.id]=time.time()

@setInterval()
def checkforspam():
  t = time.time()
  for i in uses:
    for times in uses[i]:
      pass
'''


@client.command(aliases=["helps", "menu", "menus", "pls help", "help me", "help_me", "commands"])
async def help(ctx, item=""):
    r = helps.help_command(item)
    if r == "error":
        await ctx.reply("No such command or module.")
    else:
        await ctx.send(embed=r)


@client.event
async def get_prefix(message):
    s = m.getServer(message.guild)
    return s.prefix


@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(activity=discord.Game(
        name=f"~help | {len(client.guilds)} servers!"))


@client.event
async def on_message(msg):
    if msg.content.startswith("~~copy"):
        await msg.delete()
        await msg.channel.send(msg.content[6:])

    s = m.getServer(msg.channel.guild)
    #author = msg.author.id
    #guild = msg.guild.id
    ctx = await client.get_context(msg)
    if client.user.mention in msg.content:
        await ctx.reply(f"**My prefix is  `{s.prefix}`  in this server.**",
                        embed=helps.help_command(""))

    if not msg.author.bot:
        await client.invoke(ctx)
    if s.filter_words:
        cleanmsgc = CLEAN(msg.content)
        for w in s.banned_words:
            if w in cleanmsgc or CLEAN(
                    w) in cleanmsgc or w in msg.content or CLEAN(
                        w) in msg.content:
                print(w, msg.content)
                await msg.delete()
                channel = await msg.author.create_dm()
                await channel.send(
                    f"Your message was deleted because it contained a word banned in {s.name}.\n```\n{msg.content}```\nThe word {w} is not allowed in that server."
                )
    for p in m.ported:
        if msg.channel.id == p[0] and not msg.author.bot and not msg.webhook_id:
            if len(msg.mentions)>4:
              content = re.sub(r'(?is)@.+', '', msg.content, count = len(msg.mentions)-4)
            else:content=msg.content
            past = await msg.channel.history(limit=100).flatten()
            messages = [m.content for m in past]
            num=0
            for mess in past:
              for men in mess.mentions:
                if mess.author == msg.author and men in msg.mentions:
                  num+=1
            if num > 40:
              await msg.reply(f"You have done {num} mentions in the last hundred messages.\nPlease stop mentioning so many people")
            hook = m.ported[p]
            if messages.count(msg.content)>10:
              await msg.channel.send("**Spam detected.** "+msg.author.mention )
              await msg.delete()
              break
            avatar = f"https://cdn.discordapp.com/avatars/{msg.author.id}/{msg.author.avatar}.png"
            for i in msg.attachments:
              content+=i.url
            content = content.replace("@everyone", "everyone").replace("@here", "here")
            #print("Ported", content)
            tools.send(content, msg.author.display_name, avatar, hook)
            #print("ported message")


@client.command(aliases=["invite", "info"])
async def bot_invite(ctx):
    await ctx.send(
        "**Please invite me!**\nhttps://discord.com/api/oauth2/authorize?client_id=745166643990233118&permissions=0&scope=bot"
    )


@client.event
async def on_command_error(ctx, error):
    if type(error) == commands.MissingRequiredArgument:
        return await ctx.reply(
            f"__Error:__ **Missing Required Argument: __{error.param}__.**")
    elif type(error) == commands.MissingPermissions:
        return await ctx.reply(
            f"**Missing Permission: {', '.join(error.missing_perms)}**")
    elif type(error) == commands.BotMissingPermissions:
        return await ctx.reply(
            f"**The bot is missing Permissions: {', '.join(error.missing_perms)}"
        )
    elif type(error) == commands.MissingRole:
        return await ctx.reply(
            f"**You are missing the role: {error.missing_role}")
    elif type(error) == commands.BotMissingRole:
        return await ctx.reply(
            f"The bot is lacking the role: {error.missing_role}")
    elif type(error) == commands.CommandNotFound:
        pass  #return await ctx. rep ly("That command does not exist.")
    elif type(error) == commands.CheckFailure:
        return await ctx.reply("You do not have the permissions to do that.")
    elif type(error) == commands.BadArgument:
        return await ctx.reply(str(error))
    else:
        print(
            f"{type(error)}:{error}:\n\tChannel:{ctx.message.channel}\n\tContent:{ctx.message.content}\n\tAuthor:{ctx.message.author.display_name}"
        )
        await ctx.reply(str(error))
        raise error


@commands.check(m.Checker(["administrator"]))
@client.command()
async def systemtest(ctx, test):
    await ctx.message.add_reaction("✅")


@commands.check(m.Checker(["manage_messages"]))
@client.command()
async def clear(ctx, amount=100):
    await ctx.message.channel.purge(limit=amount)
    a = await ctx.send(f"Deleted {amount} messages.")
    time.sleep(3)
    await a.delete()


@commands.check(m.Checker(["manage_guild"]))
@client.command()
async def port(ctx, channelid: Union[int, discord.TextChannel]):
    if type(channelid) == discord.TextChannel:
        channelid = channelid.id
    name = "to " + str(channelid)
    hooks = [i.name for i in await ctx.message.channel.webhooks()]
    print(name, hooks)
    if name not in hooks:
        cc = await ctx.message.channel.create_webhook(name=name)
        cc = cc.url
    else:
      for i in await ctx.message.channel.webhooks():
        if i.name==name:
          cc = i.url
          break
    m.ported[(channelid, ctx.channel.id)] = cc
    m.save()
    await ctx.reply("**Done!**")
@client.command()
async def csc(ctx):
  await ctx.reply("__CSC stands for **Cross Server Communitcation Project.**__\n\n**Status:** Ready for use. Reactions and special commands not ready.\n**Estimated time of release**: Beginning of Febuary 2022\n\n__**What is it?**__\nCSC is a project to interlink servers through a dedicated csc channel where people can chat and discover new servers. \n**Beta Link:** https://discord.com/api/oauth2/authorize?client_id=930847646606835762&permissions=535260687441&scope=bot")
@commands.check(m.Checker(["manage_guild"]))
@client.command()
async def unport(ctx, channelid: Union[int, discord.TextChannel]):
    if type(channelid) == discord.TextChannel:
        channelid = channelid.id
    m.ported.pop((channelid, ctx.channel.id))
    m.save()
    await ctx.reply("**Done!**")


client.run(getenv("Key"))
