import json
from discord import Embed

Help = Embed(title="Help Menu",
             colour=0x00ff00,
             url="https://everyones-programming-server-website.hg0428.repl.co",
             description="help [command or module]")
helpm = json.loads(open("commands.json").read())
commands = {}
for name in helpm:
    d = helpm[name]
    Help.add_field(name=name, value=', '.join(d.keys()), inline=False)
    commands[name.lower()] = Embed(title=name,
                                   description="help [command or module]",
                                   colour=0x00ff00)
    commands[name.lower()].set_footer(text="help [command or module]")
    for c in d:
        l = d[c]
        commands[name.lower()].add_field(name=c + " " + l[0],
                                         value=l[1],
                                         inline=False)
        commands[c.lower()] = Embed(title=c + " " + l[0],
                                    description=l[2],
                                    colour=0x00ff00)
        commands[c.lower()].set_footer(text="help [command or module]")

Help.set_footer(text="help [command or module]")


def help_command(item=""):
    if item == "":
        return Help
    else:
        try:
            return commands[item]
        except:
            return "error"
