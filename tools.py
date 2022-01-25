import serversett
from urllib3 import PoolManager
import json

http = PoolManager()
import discord.ext.commands as commands
import discord

m = serversett.m
import requests

embeds = m.embeds
embed_id = m.embed_id


def find(l, **kwargs):
    for n in kwargs:
        v = kwargs[n]
        for i in l:
            if getattr(i, n).lower() == v.lower():
                return i


def send(text, username, avatar_url, webhook):
    text = text.replace("@everyone", "everyone").replace("@here", "here")
    data = {"username": username, "avatar_url": avatar_url, "content": text}
    #print(webhook, data)
    requests.post(webhook, data=data)


class Embed(discord.Embed):
    def __init__(self, title, colour, link):
        self.author_object = None
        super().__init__(title=title, color=colour, url=link)


@m.client.command(aliases=["delmsg"])
@commands.check(m.Checker(["manage_messages"]))
async def delete_message(ctx, msgID: int):
    msg = await ctx.fetch_message(msgID)
    await msg.delete()


@m.client.command(aliases=["memban"])
@commands.check(m.Checker(["ban_members"]))
async def ban_member(ctx, member: discord.Member, reason="Because"):
    await member.ban(reason)


@m.client.command(aliases=["memkick"])
@commands.check(m.Checker("kick_members"))
async def kick_member(ctx, member: discord.Member, reason="Because"):
    await member.kick(reason)


@m.client.command(aliases=["sss"])
async def see_servers(ctx, server=-1):
    if server == -1:
        r = "`Servers:`"
        for s in m.SERVERS:
            s = m.SERVERS[s]
            if "invite" in s.__dict__:
                r += f"\n**__{s.name}__**\n\t{s.invite}"
    else:
        try:
            if server is int:
                s = list(m.SERVERS)[server - 1]
            else:
                s = m.SERVERS[s]
            if "invite" in s.__dict__:
                r = f"**{s.name}:**\n{s.invite}"
            else:
                raise SyntaxError
        except:
            await ctx.reply(
                "That server does not exist or is not listed. Please give a number or a server name."
            )
            return
    await ctx.send(r)


@m.client.command()
async def embed(ctx, title, description="", colour="#00ff00", link=""):
    sixteenIntegerHex = int(colour.replace("#", ""), 16)
    colour = int(hex(sixteenIntegerHex), 0)
    global embed_id
    embedVar = discord.Embed(title=title,
                             color=colour,
                             url=link,
                             description=description)
    embedVar.set_author(name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.avatar_url)
    #embedVar.author_object=ctx.message.author
    embed_id += 1
    embeds[embed_id] = embedVar
    await ctx.reply(
        f"Your embed's id is {embed_id}.\nYou can use add_embed_field to add a field to your embed.\nWhen you are ready, send your embed with send_embed. "
    )
    m.save()


@m.client.command(aliases=["aef"])
async def add_embed_field(ctx,
                          embedid: int,
                          name,
                          value,
                          inline: bool = False):
    embedVar = embeds[embedid]
    embedVar.add_field(name=name, value=value, inline=inline)
    await ctx.reply(
        f"**Done!**\nYour embed's id is {embedid}.\nYou can use add_embed_field to add a field to your embed.\nWhen you are ready, send your embed with send_embed. "
    )
    m.save()


@m.client.command()
async def send_embed(ctx, embedid: int, delete: bool = False):
    embedVar = embeds[embedid]
    await ctx.send(embed=embedVar)
    print(embedVar.author)
    if delete == True: del embeds[embedid]


@m.client.command()
async def set_embed_thumbnail(ctx, embedid, url):
    embedVar = embeds[embedid]
    embedVar.set_thumbnail(url)
    await ctx.reply("**DONE!**")


@m.client.command()
async def make_project(ctx, project_name):
    s = m.getServer(ctx.guild)
    if "project" not in s.__dict__:
        await ctx.reply(
            f"{s.name} does not have project channels set up. \nContact a moderator or admin or use ‘setup_projects‘"
        )
        return
    project = s.project
    role = await ctx.guild.create_role(name=project["rolef"].replace(
        "{name}", project_name),
                                       colour=project["colour"])
    if project["category"].lower() == "none":
        channel = ctx.message.channel.guild
    else:
        channel = find(ctx.guild.categories, name=project["category"])
    if channel == None:
        await ctx.reply(
            "That category does not exist. \nPlease ask an admin to use ‘setup_projects‘ to resetup projects with a valid category."
        )
        return None
    channel = await channel.create_text_channel(project["channelf"].replace(
        "{name}", project_name))
    perms = channel.overwrites_for(role)
    permissionstoadd = {}
    try:
        for i in project["perms"]:
            permissionstoadd[i] = True
        perms.update(**permissionstoadd)
    except Exception as e:
        await ctx.reply(
            "An error ocured in writing permissions. Please tell a mod or staff member to re setup the project channel system again and check the spelling"
        )
        raise e
    await channel.set_permissions(role, overwrite=perms)
    await ctx.message.author.add_roles(role)
    await ctx.reply("Done!")


@m.client.command()
async def search(ctx, *query):
    query = " ".join(query)
    async with ctx.channel.typing():
        resp = http.request(
            "GET", f"https://search-the-world.hg0428.repl.co/api?q={query}")
        code = json.loads(resp.data.decode('utf-8'), strict=False)
        results = dict(list(code["Results"].items())[:8])
        for r in results:
            d = results[r]
            R = discord.Embed(title=r,
                              colour=0x55ff55,
                              url=d["link"],
                              description=d["description"])
            R.set_thumbnail(url=d['favicon'])
            await ctx.send(embed=R)
        await ctx.reply(
            f"More results https://search-the-world.hg0428.repl.co/?q={query}")


@m.client.command()
async def blank(ctx, lines=75):
	if lines >200:
		await ctx.reply("Too many lines. Please enter a number less than 200.")
		return
	await ctx.send("    ‏‏‏" + "\n" * lines + "    ‏‏‏")


def sortbytime(obj):
    return obj.created_at

@commands.check(m.Checker("manage_channels"))
@m.client.command()
async def mergechannels(ctx, newname, limit:int,*channels: discord.TextChannel):
    newchannel = await ctx.guild.create_text_channel(newname)
    webhook = await newchannel.create_webhook(name="YouCanDeleteThis WhenNoNewMessagesAreBeingSent")
    for channel in channels:
      async for message in ctx.channel.history(limit=limit):
        send(message.content, message.author.display_name, str(message.author.avatar_url), webhook.url)
      #await channel.delete()
    await ctx.reply("**Done!**")
    await newchannel.send(f"{ctx.message.author.mention}")
    
