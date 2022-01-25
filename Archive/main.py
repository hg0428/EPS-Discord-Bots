import ka
import os
import time
import discord
from help import *
from m import *
client.remove_command("help")
bad_words = os.getenv("Bad_words").split(",")
import serversett
serversett.init(client)
admin = [676414144643203120]


def fix(f="main.py"):
    a = open(f).read()
    open(f, "w").write(a.replace(" " * 2, "\t"))


#fix("m.py")
#fix()
@client.event
async def get_prefix(bot, message):
    guild = message.guild
    # you can do something here with the guild obj, open a file and return something different per guild
    return ":"


client = commands.Bot(command_prefix=get_prefix)


@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
                                  name=f"to {len(client.guilds)} servers!"))
    print("Presence Changed!")


@client.event
async def on_message(msg):
    if msg.content.startswith("~~copy"):
        await msg.delete()
        await msg.channel.send(msg.content[6:])
    author = msg.author.id
    guild = msg.guild.id
    ctx = await client.get_context(msg)
    await client.invoke(ctx)


client.remove_command("help")


@client.command()
async def bot_invite(ctx):
    await ctx.send(
        "**Please invite me!**\nhttps://discord.com/api/oauth2/authorize?client_id=745166643990233118&permissions=0&scope=bot"
    )


@client.command()
async def help(ctx, module=""):
    if module == "":
        embedVar = discord.Embed(title="Help",
                                 color=0x00ff00,
                                 url="https://EPS-Discord-Bots.hg0428.repl.co")
        embedVar.set_author(name="AmazingActiveProgrammingBot",
                            icon_url=client.user.avatar_url)
        for h in helps:
            embedVar = h.addto(embedVar)
    else:
        embedVar = discord.Embed(title="Help",
                                 color=0x00ff00,
                                 url="https://EPS-Discord-Bots.hg0428.repl.co")
        embedVar.set_author(name="AmazingActiveProgrammingBot",
                            icon_url=client.user.avatar_url)
        embedVar = helps[module].addto(embedVar)
    await ctx.send(embed=embedVar)


@client.command()
async def eval(ctx, thing):
    if ctx.message.author.id in admin:
        try:
            exec(thing)
            #await ctx.send(str(a))
        except Exception as exc:
            await ctx.send(type(exc).__name__ + ": " + str(exc))
    else:
        await ctx.send("**Error#03: Not admin!**")


@client.command()
async def clear(ctx, amount=100):
    perms = ctx.message.author.guild_permissions
    if perms.manage_messages or ctx.message.author.id in admin:
        await ctx.message.channel.purge(limit=amount)
        a = await ctx.send(f"Deleted {amount} messages.")
        time.sleep(3)

        await a.delete()
    else:
        await ctx.send("You do not have the permissions")


@client.command()
async def suggest(ctx, title):
    open("DATA/suggest", "a").write(title.replace("\n", "\\n") + "\r\n")
    await ctx.send("Thanks!")


@client.command()
async def invites(ctx, user: discord.Member):
    if user == "": user = ctx.message.author
    total = 0
    message = ctx.message
    try:
        await message.guild.invites()
    except:
        ctx.send("I do not have the permissions to see the invites")
    for i in await message.guild.invites():
        if i.inviter == user:
            total += i.uses
    embed = discord.Embed(
        title="Information",
        color=0x00ff00,
        description=
        f"{user.mention} has invited {total} users to {ctx.message.channel.guild.name}."
    )
    embed.set_author(name=user.display_name, icon_url=user.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def get_invite(ctx, guild_name=""):

    if guild_name != "":
        guild = []
        for g in client.guilds:
            if g.name.lower().startswith(guild_name.lower()) or str(
                    g.id).startswith(guild_name):
                guild.append(g)
        if len(guild) == 1: guild = guild[0]
        elif len(guild) > 1:
            await ctx.send("\n".join(f"**{g.name}**" + "\n*or*"
                                     for g in guild))
            return
        elif guild == []:
            await ctx.send("Not found")
            return
    else:
        guild = ctx.message.channel.guild
    for t in guild.text_channels:
        try:
            await ctx.send(await t.create_invite(max_age=300))
            return
        except Exception as e:
            print(e)
    await ctx.send("I dont have the permissions to do that.")


@client.command()
async def list_servers(ctx):
    text = ""
    for s in client.guilds:
        text += f"**{s.name}**: *{s.id}*\n\n"
    await ctx.send(text)


ka.keep_alive()
client.run(os.getenv("Key"))
