import discord
from discord.ext.commands import check
import m


@check(m.Checker(["administrator"]))
@m.client.command()
async def set_rules(ctx, *args):
	server = m.getServer(ctx.message.channel.guild)
	server.rules = args
	m.save()
	await rules(ctx)


@m.client.command(aliases=['rule'])
async def rules(ctx, number=-1):
	server = m.getServer(ctx.message.channel.guild)
	embedVar = discord.Embed(title=f"{server.name} – Rules",
	                         color=0x00ff00,
	                         url="https://EPS-Discord-Bots.hg0428.repl.co")
	embedVar.set_author(name=ctx.message.author.display_name,
	                    icon_url=ctx.message.author.avatar_url)
	if number == -1:
		for i in range(len(server.rules)):
			embedVar.add_field(name=f"{i+1}",
			                   value=server.rules[i],
			                   inline=False)
	else:
		embedVar.add_field(name=f"{number}",
		                   value=server.rules[number],
		                   inline=False)
	await ctx.send(embed=embedVar)


@check(m.Checker(["manage_guild"]))
@m.client.command()
async def set_prefix(ctx, new_prefix):
	s = m.getServer(ctx.message.channel.guild)
	s.prefix = new_prefix
	await ctx.reply("Done!")
	m.save()


@check(m.Checker(["administrator"]))
@m.client.command(aliases=["twfilter"])
async def toggle_word_filter(ctx):
	s = m.getServer(ctx.message.channel.guild)
	s.filter_words = not s.filter_words
	await ctx.reply(
	    f"**Filter: {s.filter_words}**\nSet filtered words with `set_filter_words`"
	)
	m.save()


@check(m.Checker(["administrator"]))
@m.client.command(aliases=["sfwords"])
async def set_filter_words(ctx, *args):
	s = m.getServer(ctx.message.channel.guild)
	s.banned_words = args
	await ctx.reply("**Done!**")
	m.save()


@check(m.Checker(["administrator"]))
@m.client.command()
async def list_server(ctx):
	invite = await ctx.channel.create_invite()
	s = m.getServer(ctx.channel.guild)
	s.invite = invite.url
	await ctx.reply("**Done!**")
	m.save()


@check(m.Checker(["administrator"]))
@m.client.command()
async def ban_word(ctx, word: str):
	s = m.getServer(ctx.channel.guild)
	s.banned_words = list(s.banned_words)
	s.banned_words.append(word)
	await ctx.reply("The word has been banned.")
	m.save()


@check(m.Checker(["administrator"]))
@m.client.command()
async def unban_word(ctx, word: str):
	s = m.getServer(ctx.channel.guild)
	s.banned_words = list(s.banned_words)
	list(s.banned_words).remove(word)
	await ctx.reply("The word has been unbanned.")
	m.save()


@m.client.command()
async def setup_projects(ctx):
	s = m.getServer(ctx.message.guild)
	rolef = await ctx.reply(
	    "**What format would you like for project roles?**\n Use `{name}` in place of the project name. Reply to this message with your answer."
	)
	rolef = await m.client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == rolef.id)
	channelf = await ctx.reply(
	    "**What format would you like for project channels?**\n Use `{name}` in place of the project name. Reply to this message with your answer."
	)
	channelf = await m.client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == channelf.id)
	role_colour = await ctx.reply(
	    "**What colour would you like to use for project roles?**\nPlease use hex. Reply to this message with your answer. "
	)
	role_colour = await m.client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == role_colour.id)
	role_colour = int(role_colour.content.replace("#", ""), 16)
	perms = await ctx.reply(
	    "**What permissions would you like to give project owners in their project channel?**\nSeparate with newline. These permissions only apply for the people with the project role and only work in the project channel. \n Use `all` for all permissions or `none` for no extra permissions. \nReply to this message with your answer."
	)
	perms = await m.client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == perms.id)
	category = await ctx.reply(
	    "**What category would you like project channels to be added to?**\nPut ‘none‘ for none.\n Reply to this message with your answer."
	)
	category = await m.client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == category.id)
	if "project" not in s.__dict__: s.project = {}
	s.project["rolef"] = rolef.content
	s.project["channelf"] = channelf.content
	s.project["perms"] = m.pppppperms(perms.content)
	s.project["colour"] = role_colour
	s.project["category"] = category.content.upper()
	m.save()
	await ctx.reply(f"**Project channels are now set up for {s.name}**")


@m.client.command(aliases=["adchall"])
async def addchallenge(ctx, name, description):
	e = discord.Embed(title=name,
	                  description=description,
	                  colour=ctx.message.author.colour)
	e.set_author(name=ctx.message.author.display_name,
	             icon_url=ctx.message.author.avatar_url)
	await ctx.message.delete()
	await ctx.send(embed=e)
