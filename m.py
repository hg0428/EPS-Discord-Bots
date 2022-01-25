import os
import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button

client = commands.Bot(command_prefix="~")
DiscordComponents(client)
from pickle import dump, load, HIGHEST_PROTOCOL

admin = open("admin.txt").read()
admin = [int(i) for i in admin.split("\n")]


def EditDistance(s1, s2):
	if len(s1) > len(s2):
		s1, s2 = s2, s1

	distances = range(len(s1) + 1)
	for i2, c2 in enumerate(s2):
		distances_ = [i2 + 1]
		for i1, c1 in enumerate(s1):
			if c1 == c2:
				distances_.append(distances[i1])
			else:
				distances_.append(1 + min((distances[i1], distances[i1 + 1],
				                           distances_[-1])))
		distances = distances_
	return distances[-1]


perms = [
    "add_reactions", "administrator", "attach_files", "ban_members",
    "change_nickname", "connect", "create_instant_invite", "deafen_members",
    "embed_links", "external_emojis", "kick_members", "manage_channels",
    "manage_emojis", "manage_guild", "manage_messages", "manage_nicknames",
    "manage_permissions", "manage_roles", "manage_webhooks",
    "mention_everyone", "move_members", "mute_members", "priority_speaker",
    "read_message_history", "read_messages", "request_to_speak",
    "send_messages", "send_tts_messages", "speak", "stream",
    "use_external_emojis", "use_slash_commands", "use_voice_activation",
    "view_audit_log", "view_channel", "view_guild_insights"
]


def pppppperms(sent):
	sent = " ".join(sent.lower().split()).split("\n")
	returned = []
	for i in sent:
		if i in perms:
			returned += i
		else:
			i.replace("server", "guild")
			if i in perms: returned += i
			else:
				best = 99
				num1 = ""
				for perm in perms:
					e = EditDistance(perm, i)
					if e < best:
						num1 = perm
						best = e
				if num1 != "" and best < 3: returned += num1
	print(returned)
	return returned


def encode(text, key=5):
	ntext = ""
	for i in text:
		ntext += chr(ord(i) + key)
	return ntext


def decode(text, key=5):
	ntext = ""
	for i in text:
		ntext += chr(ord(i) - key)
	return ntext


bad_words = list(decode(os.getenv("Bad_words")).split(","))


async def ask(what, ctx):
	question = await ctx.reply(what)
	answer = await client.wait_for(
	    "message",
	    check=lambda message: message.reference != None and message.reference.
	    message_id == question.id)
	return answer


#bad_words.replace(",ass", ",asshole")
#print(encode(bad_words))
def amountof(obj, l):
	number = 0
	for i in l:
		if i == obj: number += 1
	return number


class Checker:
	def __init__(self, auth, amount=-1):
		if type(auth) == str:
			auth = [auth]
		self.auth = auth
		self.amount = amount

	def __call__(self, ctx):
		try:
			ctx.message
		except:
			return
		print(self.auth)
		if ctx.message.author.id in admin:
			print("Interaction with Admin")
			return True
		true = []
		for a in self.auth:
			try:
				print(a)
				true.append(getattr(ctx.message.author.guild_permissions, a))
				print(a)
			except:
				return
		if self.amount == -1 and true == [True] * len(self.auth):
			return True
		else:
			if self.amount == amountof(True, true):
				return True
		return False


class Server:
	def __init__(self, sid, name):
		self.id, self.name, self.prefix, self.rules = sid, name, "~", {}
		self.banned_words = bad_words
		self.filter_words = False
		SERVERS[sid] = self


def save():
	save_object(SERVERS, "servers.pkl")
	save_object(embeds, "embeds.pkl")
	save_object(ported, "ported.pkl")


def save_object(obj, filename):
	with open(filename, 'wb+') as output:  # Overwrites any existing file.
		dump(obj, output, HIGHEST_PROTOCOL)


def load_object(filename, default):
	try:
		with open(filename, "rb") as input:
			return load(input)
	except:
		return default


def getServer(guild):
	try:
		return SERVERS[guild.id]
	except:
		s = Server(guild.id, guild.name)
		save()
		return s


SERVERS = load_object("servers.pkl", {})
embeds = load_object("embeds.pkl", {})
embed_id = len(embeds)
ported = load_object("ported.pkl", {})
save()
