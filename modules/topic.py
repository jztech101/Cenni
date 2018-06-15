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

def getChanSplitChar(cenni, a):
    if hasattr(cenni.config, 'topicsplit'):
        if a in cenni.config.topicsplit:
            return cenni.config.topicsplit[a]
        else:
            return

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
    index = 1
    if tools.isChan(text[1], False):
        if argc < 2: return
        channel = text[1]
        topic = ' '.join(text[2:])
        index = 2
    if not is_chan_admin(cenni,input,channel):
        return cenni.say('You must be an admin to perform this operation')
    if channel not in cenni.channeltopics:
        currenttopic = None
    else:
        currenttopic = cenni.channeltopics[channel]
    if currenttopic and getChanSplitChar(cenni, channel) and (len(text) > index+1 or text[index].startswith("-")):
        char = getChanSplitChar(cenni, channel)
        if text[index].startswith("-") and  "".join(text[index][1:]).isdigit() and len(currenttopic.split(char)) >= int("".join(text[index][1:])):
           tmp = currenttopic.split(char)
           tmp.pop(int("".join(text[index][1:]))-1)
           currenttopic = char.join(tmp)
        elif text[index].isdigit() and len(currenttopic.split(char)) >= int(text[index]):
           tmp = currenttopic.split(char)
           tmp[int(text[index])-1] = ' '.join(text[index+1:])
           currenttopic = char.join(tmp)
        elif text[index] == 'add':
           tmp = currenttopic.split(char)
           tmp.append(' '.join(text[index+1:]))
           currenttopic = char.join(tmp)
        else:
           currenttopic = topic
        cenni.write(['TOPIC', channel], currenttopic)
    else:
        cenni.write(['TOPIC', channel], topic)
    return
topic.commands = ['topic']
topic.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
