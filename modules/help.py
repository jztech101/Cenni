
def doc(cenni, input):
    """Shows a command's documentation, and possibly an example."""
    if input.group(2):
        name = input.group(2)
        if name and name in cenni.doc:
            cenni.say(cenni.doc[name][0])
            if cenni.doc[name][1]:
                cenni.say('e.g. ' + cenni.doc[name][1])
        else:
            cenni.say('No help found')
    else:
        cenni.say('User Commands: shrug, moo, cookie, source, potato, burn | ping, pong | seen | version | sc | geoip, who | Admin Commands: op, deop, voice, devoice, quiet, unquiet, ban, unban, kickban (kb, kban), invite, kick')
doc.commands = ['help', 'commands']
doc.example = 'help'
doc.priority = 'low'
