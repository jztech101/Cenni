#!/usr/bin/env python3
import threading, time, sys
import tools

def setup(cenni):
    # by clsn
    cenni.data = {}
    refresh_delay = 300.0

    if hasattr(cenni.config, 'refresh_delay'):
        try: refresh_delay = float(cenni.config.refresh_delay)
        except: pass

        def close():
            print("Nobody PONGed our PING, restarting")
            cenni.handle_close()

        def pingloop():
            timer = threading.Timer(refresh_delay, close, ())
            cenni.data['startup.setup.timer'] = timer
            cenni.data['startup.setup.timer'].start()
            # print "PING!"
            cenni.write(('PING', cenni.config.host))
        cenni.data['startup.setup.pingloop'] = pingloop

        def pong(cenni, input):
            try:
                # print "PONG!"
                cenni.data['startup.setup.timer'].cancel()
                time.sleep(refresh_delay + 60.0)
                pingloop()
            except: pass
        pong.event = 'PONG'
        pong.thread = True
        pong.rule = r'.*'
        cenni.variables['pong'] = pong

        # Need to wrap handle_connect to start the loop.
        inner_handle_connect = cenni.handle_connect

        def outer_handle_connect():
            inner_handle_connect()
            if cenni.data.get('startup.setup.pingloop'):
                cenni.data['startup.setup.pingloop']()

        cenni.handle_connect = outer_handle_connect

def nick(cenni,input):
   oldnick = input.nick.lower()
   newnick = input.sender.replace(":","").lower()
   if oldnick == newnick:
       return
   cenni.set_hostmask(newnick, cenni.hostmasks[oldnick])
   cenni.set_ident(newnick, cenni.idents[oldnick])
   cenni.set_ipaddr(newnick, cenni.ipaddrs[oldnick])
   cenni.set_account(newnick, cenni.accounts[oldnick])
   cenni.set_server(newnick, cenni.servers[oldnick])
   cenni.set_realname(newnick, cenni.realnames[oldnick])
   cenni.del_hostmask(oldnick)
   cenni.del_ident(oldnick)
   cenni.del_ipaddr(oldnick)
   cenni.del_account(oldnick)
   cenni.del_server(oldnick)
   cenni.del_realname(oldnick)
   for channel in cenni.channels:
       if channel in cenni.ops and oldnick in cenni.ops[channel]:
           cenni.del_op(channel, oldnick)
           cenni.add_op(channel, newnick)
       if channel in cenni.hops and oldnick in cenni.hops[channel]:
           cenni.add_halfop(channel, newnick)
           cenni.del_halfop(channel, oldnick)
       if channel in cenni.voices and oldnick in cenni.voices[channel]:
           cenni.add_voice(channel,  newnick)
           cenni.del_voice(channel,  oldnick)
       cenni.del_user(channel, oldnick)
       cenni.add_user(channel, newnick)
nick.rule = r'(.*)'
nick.event = 'NICK'
nick.priority = 'high'

def startup(cenni, input):
    import time

    if hasattr(cenni.config, 'serverpass') and not cenni.auth_attempted:
        cenni.write(('PASS', cenni.config.serverpass))

    if not cenni.is_authenticated and hasattr(cenni.config, 'password'):
        if hasattr(cenni.config, 'user') and cenni.config.user is not None:
            user = cenni.config.user
        else:
            user = cenni.config.nick

        cenni.msg('NickServ', 'IDENTIFY %s %s' % (user, cenni.config.password))
        time.sleep(10)

    # Cf. http://swhack.com/logs/2005-12-05#T19-32-36
    for channel in cenni.channels:
       cenni.join(channel, None)
       time.sleep(0.7)
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

# Method for populating op/hop/voice information in channels on join
def privs_on_join(cenni, input):
    if not input.mode_target or not tools.isChan(input.mode_target, False):
        return
    channel = input.mode_target
    if input.names and len(input.names) > 0:
        split_names = input.names.split()
        for name in split_names:
            nick_mode, nick = name[0], name[1:].lower()
            if nick_mode == '@':
                cenni.add_op(channel, nick)
            elif nick_mode == '%':
                cenni.add_halfop(channel, nick)
            elif nick_mode == '+':
                cenni.add_voice(channel,  nick)
            if nick_mode.isalnum():
                cenni.add_user(channel, name)
            else:
                cenni.add_user(channel, nick)
privs_on_join.rule = r'(.*)'
privs_on_join.event = '353'
privs_on_join.priority = 'high'

def whoo(cenni, input):
    if not input.mode or not tools.isChan(input.mode, False):
        return
    nick = input.other2.lower()
    cenni.set_hostmask(nick, input.names)
    cenni.set_ident(nick, input.mode_target)
    cenni.set_server(nick, input.other)
    cenni.set_realname(nick, input.other3)
whoo.rule = r'(.*)'
whoo.event = '352'
whoo.priority = 'high'

def whox(cenni, input):
    nick = input.other4.lower()
    cenni.set_hostmask(nick, input.other)
    cenni.set_ident(nick, input.mode_target)
    cenni.set_ipaddr(nick, input.names)
    cenni.set_account(nick, input.other6)
    cenni.set_server(nick,input.other2)
    cenni.set_realname(nick, input.rest)
whox.rule = r'(.*)'
whox.event = '354'
whox.priority = 'high'

def new_Join_Hostmask(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    cenni.write(['WHO', input.sender, '%cuhsnfair'])
    cenni.add_user(input.sender, input.nick.lower())
new_Join_Hostmask.rule = r'(.*)'
new_Join_Hostmask.event = 'JOIN'
new_Join_Hostmask.priority = 'high'

def PartE(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    channel = input.sender
    nick = input.nick.lower()
    if channel in cenni.ops and nick in cenni.ops[channel]:
        cenni.del_op(channel, nick)
    if channel in cenni.hops and nick in cenni.hops[channel]:
        cenni.del_halfop(channel, nick)
    if channel in cenni.voices and nick in cenni.voices[channel]:
        cenni.del_voice(channel,  nick)
    cenni.del_user(channel, nick)
PartE.rule = r'(.*)'
PartE.event = 'PART'
PartE.priority = 'high'

def KickE(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    channel = input.sender
    nick = input.mode.lower
    if channel in cenni.ops and nick in cenni.ops[channel]:
        cenni.del_op(channel, nick)
    if channel in cenni.hops and nick in cenni.hops[channel]:
        cenni.del_halfop(channel, nick)
    if channel in cenni.voices and nick in cenni.voices[channel]:
        cenni.del_voice(channel,  nick)
    cenni.del_user(channel, nick)
KickE.rule = r'(.*)'
KickE.event = 'KICK'
KickE.priority = 'high'

def QuitE(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    channel = input.sender
    nick = input.nick.lower()
    for channel in cenni.channels:
        if channel in cenni.ops and nick in cenni.ops[channel]:
            cenni.del_op(channel, nick)
        if channel in cenni.hops and nick in cenni.hops[channel]:
            cenni.del_halfop(channel, nick)
        if channel in cenni.voices and nick in cenni.voices[channel]:
            cenni.del_voice(channel,  nick)
        cenni.del_user(channel, nick)
QuitE.rule = r'(.*)'
QuitE.event = 'QUIT'
QuitE.priority = 'high'

# Method for tracking changes to ops/hops/voices in channels
def track_priv_change(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return

    channel = input.sender

    if input.mode:
        add_mode = input.mode.startswith('+')
        del_mode = input.mode.startswith('-')

        # Check that this is a mode change and that it is a mode change on a user
        if (add_mode or del_mode) and input.mode_target and len(input.mode_target) > 0:
            mode_change = input.mode[1:]
            mode_target = input.mode_target.lower()

            if add_mode:
                if mode_change == 'o':
                    cenni.add_op(channel, mode_target)
                elif mode_change == 'h':
                    cenni.add_halfop(channel, mode_target)
                elif mode_change == 'v':
                    cenni.add_voice(channel, mode_target)
            else:
                if mode_change == 'o':
                    cenni.del_op(channel, mode_target)
                elif mode_change == 'h':
                    cenni.del_halfop(channel, mode_target)
                elif mode_change == 'v':
                    cenni.del_voice(channel, mode_target)
track_priv_change.rule = r'(.*)'
track_priv_change.event = 'MODE'
track_priv_change.priority = 'high'

if __name__ == '__main__':
    print(__doc__.strip())
