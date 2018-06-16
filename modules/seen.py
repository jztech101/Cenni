#!/usr/bin/env python3
import time
import tools

def f_seen(cenni, input):
    """.seen <nick> - Reports when <nick> was last seen."""

    if not input.group(2):
        return cenni.say('Please provide a nick.')
    nick = input.group(2).lower()

    if not hasattr(cenni, 'seen'):
        return cenni.say('?')

    if nick in cenni.seen:
        channel, t = cenni.seen[nick]
        t = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(t))
        msg = 'I last saw %s at %s in some channel.' % (nick, t)
        cenni.say(msg)
    else:
        cenni.say("Sorry, I haven't seen %s around." % nick)
f_seen.commands = ['seen']

def f_note(cenni, input):
    try:
        if not hasattr(cenni, 'seen'):
            cenni.seen = dict()
        if tools.isChan(input.sender, False):
            cenni.seen[input.nick.lower()] = (input.sender, time.time())
    except Exception as e: print(e)
f_note.rule = r'(.*)'
f_note.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
