helps = []


class Help:
    def __init__(self, title, use, description):
        self.title = title
        self.use = use
        self.description = description
        helps.append(self)

    def addto(self, embed):
        embed.add_field(
            name=f"**{self.title}**",
            value=f"**{self.use}**\n{self.description}",
            inline=False)
        return embed


Help("Help", "help [command or module]",
     "Gives descriptions of commands and modules available on this bot.")
Help("Suggest", "suggest <suggestion>", "Sends a suggestion.")
Help("Clear", "clear [limit=100]",
     "Deletes all messages in that channel up until the limit.")
Help("Invites", "invites <user>",
     "Tells how many people the user has invited to the server.")
Help("Get Invite", "get_invite <server name>", "Gets the invite for the specified server (not case sensitive).")
Help("Invite Bot", "bot_invite", "Gets the bot's invite link.")
Help("List Servers", "list_servers", "Lists all the servers the bot is in")