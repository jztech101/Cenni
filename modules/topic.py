#!/usr/bin/env python3
import re
import tools

def is_chan_admin(cenni, input, a):
    if input.admin:
        return True
    elif hasattr(cenni.config, 'helpers'):
        if a in cenni.config.helpers and input.host in cenni.config.helpers[a]:
            return True
    return False

def topic(cenni, input):
    """
    This gives admins the ability to change the topic.
    Note: One does *NOT* have to be an OP, one just has to be on the list of
    admins.
    """
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    topic = ' '.join(text[1:])
    if tools.isChan(text[1], False):
        if argc < 2: return
        channel = text[1]
        topic = ' '.join(text[2:])
    if not is_chan_admin(cenni,input,channel):
        return cenni.say('You must be an admin to perform this operation')
    if topic == '':
        return
    cenni.write(['TOPIC', channel], topic)
    return
topic.commands = ['topic']
topic.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
