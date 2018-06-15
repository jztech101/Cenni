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

def voice(cenni, input):
    """
    Command to voice users in a room. If no nick is given,
    cenni will voice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['MODE', channel, "+v", nick])
voice.commands = ['voice']
voice.priority = 'low'
voice.example = '.voice ##example or .voice ##example nick'

def mode(cenni, input):
    """
    """
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                modex = " ".join(text[2:])
        else:
            modex = " ".join(text[1:])
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['MODE', channel, modex])
mode.commands = ['mode']
mode.priority = 'low'

def invite(cenni, input):
    """
    Command to voice users in a room. If no nick is given,
    cenni will voice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['PRIVMSG', channel], '\x01ACTION invites ' + nick + ' per ' + input.nick + '\x01')
        cenni.write(['INVITE', nick], channel)
invite.commands = ['invite']
invite.priority = 'low'

def devoice(cenni, input):
    """
    Command to devoice users in a room. If no nick is given,
    cenni will devoice the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['MODE', channel, "-v", nick])
devoice.commands = ['devoice']
devoice.priority = 'low'
devoice.example = '.devoice ##example or .devoice ##example nick'

def op(cenni, input):
    """
    Command to op users in a room. If no nick is given,
    cenni will op the nick who sent the command
    """
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['MODE', channel, "+o", nick])
op.commands = ['op']
op.priority = 'low'
op.example = '.op ##example or .op ##example nick'

def deop(cenni, input):
    text = input.group().split()
    argc = len(text)
    nick = input.nick
    channel = input.sender
    if not tools.isChan(input.sender, False):
        channel = None
    if argc >= 2 and text[1] is not None:
        if tools.isChan(text[1], False):
            channel = text[1]
            if argc >= 3 and text[2] is not None:
                nick = text[2]
        else:
            nick = text[1]
    if channel is not None:
        if not is_chan_admin(cenni,input,channel):
            return cenni.say('You must be an admin to perform this operation')
        cenni.write(['MODE', channel, "-o", nick])
deop.commands = ['deop']
deop.priority = 'low'
deop.example = '.deop ##example or .deop ##example nick'

def kick(cenni, input):
    text = input.group().split()
    argc = len(text)
    channel = input.sender
    opt = text[1]
    nick = opt
    reasonidx = "Your behavior is not conductive to the desired environment"
    if tools.isChan(opt, False):
        channel = opt
        nick = text[2]
        if (argc > 3):
            reasonidx = " ".join(text[3:])
    else:
        if (argc > 2):
            reasonidx = " ".join(text[2:])
    if not is_chan_admin(cenni, input, channel):
        return cenni.say('You must be an admin to perform this operation')
    if "," in nick:
        nicks = nick.split(",")
        for nic in nicks:
            kickx(cenni, channel, nic, input.nick, reasonidx)
    else:
        kickx(cenni, channel, nick, input.nick, reasonidx)
kick.commands = ['kick']
kick.priority = 'high'

def kickx(cenni, channel, nick, sender, reasonidx):
    if nick == cenni.nick:
        nick = sender
    cenni.write(['KICK', channel, nick, ' :', "[" + sender + "] " + reasonidx])

def configureHostMask (mask, cenni):
    if "!" not in mask and "@" not in mask and ":" not in mask:
        ident = cenni.idents[mask]
        host = cenni.hostmasks[mask]
        if "~" not in ident:
            return "*!" + ident + "@" + host
        else:
            return "*!*@" + host
    else:
        return mask

def ban (cenni, input):
    """
    This give admins the ability to ban a user.
    The bot must be a Channel Operator for this command to work.
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    banmask = opt
    channel = input.sender
    if tools.isChan(opt, False):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(cenni,input,channel):
        return cenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, cenni)
    if banmask == '': return
    cenni.write(['MODE', channel, '+b', banmask])
ban.commands = ['ban']
ban.priority = 'high'

def unban (cenni, input):
    """
    This give admins the ability to unban a user.
    The bot must be a Channel Operator for this command to work.
    """
    text = input.group().split()
    argc = len(text)
    if argc < 2: return
    opt = text[1]
    banmask = opt
    channel = input.sender
    if tools.isChan(opt, False):
        if argc < 3: return
        channel = opt
        banmask = text[2]
    if not is_chan_admin(cenni,input,channel):
        return cenni.say('You must be an admin to perform this operation')
    banmask = configureHostMask(banmask, cenni)
    if banmask == '': return
    cenni.write(['MODE', channel, '-b', banmask])
unban.commands = ['unban']
unban.priority = 'high'

def quiet (cenni, input):
   """
   This gives admins the ability to quiet a user.
   The bot must be a Channel Operator for this command to work
   """
   text = input.group().split()
   argc = len(text)
   if argc < 2: return
   opt = text[1]
   banmask = opt
   channel = input.sender
   if tools.isChan(opt, False):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(cenni, input, channel):
       return cenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, cenni)
   if quietmask == '': return
   cenni.write(['MODE', channel, '+q', quietmask])
quiet.commands = ['quiet']
quiet.priority = 'high'

def unquiet (cenni, input):
   """
   This gives admins the ability to unquiet a user.
   The bot must be a Channel Operator for this command to work
   """
   text = input.group().split()
   argc = len(text)
   if argc < 2: return
   opt = text[1]
   banmask = opt
   channel = input.sender
   if tools.isChan(opt, False):
       if argc < 3: return
       channel = opt
       banmask = text[2]
   if not is_chan_admin(cenni, input, channel):
       return cenni.say('You must be an admin to perform this operation')
   quietmask = configureHostMask(banmask, cenni)
   if quietmask == '': return
   cenni.write(['MODE', channel, '-q', quietmask])
unquiet.commands = ['unquiet']
unquiet.priority = 'high'

def kickban (cenni, input):
   """
   This gives admins the ability to kickban a user.
   The bot must be a Channel Operator for this command to work
   .kickban [#chan] user1 user!*@* get out of here
   """
   text = input.group().split()
   argc = len(text)
   channel = input.sender
   opt = text[1]
   nick = opt
   reasonidx = "Your behavior is not conductive to the desired environment"
   if tools.isChan(opt, False):
       channel = opt
       nick = text[2]
       if(argc >3):
           reasonidx = " ".join(text[3:])
   else:
       if(argc >2):
           reasonidx = " ".join(text[2:])
   if not is_chan_admin(cenni, input, channel):
       return cenni.say('You must be an admin to perform this operation')
   mask = configureHostMask(nick,cenni)
   if mask == '': return
   cenni.write(['MODE', channel, '+b', mask])
   kickx(cenni, channel, nick, input.nick, reasonidx)
kickban.commands = ['kickban', 'kb', 'kban']
kickban.priority = 'high'

if __name__ == '__main__':
    print(__doc__.strip())
