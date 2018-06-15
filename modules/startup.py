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
        time.sleep(0.5)
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
            nick_mode, nick = name[0], name[1:]
            if nick_mode == '@':
                cenni.add_op(channel, nick)
            elif nick_mode == '%':
                cenni.add_halfop(channel, nick)
            elif nick_mode == '+':
                cenni.add_voice(channel, nick_mode + nick)
privs_on_join.rule = r'(.*)'
privs_on_join.event = '353'
privs_on_join.priority = 'high'

def hostmask_on_join(cenni, input):
    if not input.mode or not tools.isChan(input.mode, False):
        return
    cenni.set_hostmask(input.other2, input.names)
    cenni.set_ident(input.other2, input.mode_target)
hostmask_on_join.rule = r'(.*)'
hostmask_on_join.event = '352'
hostmask_on_join.priority = 'high'

def new_Join_Hostmask(cenni, input):
    if not input.sender or not tools.isChan(input.sender, False):
        return
    cenni.set_hostmask(input.nick, input.host)
    cenni.set_ident(input.nick, input.user)
new_Join_Hostmask.rule = r'(.*)'
new_Join_Hostmask.event = 'JOIN'
new_Join_Hostmask.priority = 'high'

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
            mode_target = input.mode_target

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
