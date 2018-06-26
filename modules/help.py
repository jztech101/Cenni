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
        cenni.say('help: returns maybe helpful information')
doc.commands = ['help']
doc.example = 'help'
doc.priority = 'low'
