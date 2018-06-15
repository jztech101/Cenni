#!/usr/bin/env python3
import base64

def irc_cap (cenni, input):
    cap, value = input.args[1], input.args[2]
    rq = ''

    if cenni.is_connected:
        return

    if cap == 'LS':
        if 'multi-prefix' in value:
            rq += ' multi-prefix'
        if 'sasl' in value:
            rq += ' sasl'

        if not rq:
            irc_cap_end(cenni, input)
        else:
            if rq[0] == ' ':
                rq = rq[1:]

            cenni.write(('CAP', 'REQ', ':' + rq))

    elif cap == 'ACK':
        if 'sasl' in value:
            cenni.write(('AUTHENTICATE', 'PLAIN'))
        else:
            irc_cap_end(cenni, input)

    elif cap == 'NAK':
        irc_cap_end(cenni, input)

    else:
        irc_cap_end(cenni, input)

    return
irc_cap.rule = r'(.*)'
irc_cap.event = 'CAP'
irc_cap.priority = 'high'


def irc_authenticated (cenni, input):
    auth = False
    if hasattr(cenni.config, 'nick') and cenni.config.nick is not None and hasattr(cenni.config, 'password') and cenni.config.password is not None:
        nick = cenni.config.nick
        password = cenni.config.password

        # If provided, use the specified user for authentication, otherwise just use the nick
        if hasattr(cenni.config, 'user') and cenni.config.user is not None:
            user = cenni.config.user
        else:
            user = nick

        auth = "\0".join((nick, user, password))
        auth = base64.b64encode(auth.encode('utf-8'))

    if not auth:
        cenni.write(('AUTHENTICATE', '+'))
    else:
        while len(auth) >= 400:
            out = auth[0:400]
            auth = auth[401:]
            cenni.write(('AUTHENTICATE', out))

        if auth:
            cenni.write(('AUTHENTICATE', auth))
        else:
            cenni.write(('AUTHENTICATE', '+'))

    return
irc_authenticated.rule = r'(.*)'
irc_authenticated.event = 'AUTHENTICATE'
irc_authenticated.priority = 'high'


def irc_903 (cenni, input):
    cenni.is_authenticated = True
    irc_cap_end(cenni, input)
    return
irc_903.rule = r'(.*)'
irc_903.event = '903'
irc_903.priority = 'high'


def irc_904 (cenni, input):
    irc_cap_end(cenni, input)
    return
irc_904.rule = r'(.*)'
irc_904.event = '904'
irc_904.priority = 'high'


def irc_905 (cenni, input):
    irc_cap_end(cenni, input)
    return
irc_905.rule = r'(.*)'
irc_905.event = '905'
irc_905.priority = 'high'


def irc_906 (cenni, input):
    irc_cap_end(cenni, input)
    return
irc_906.rule = r'(.*)'
irc_906.event = '906'
irc_906.priority = 'high'


def irc_907 (cenni, input):
    irc_cap_end(cenni, input)
    return
irc_907.rule = r'(.*)'
irc_907.event = '907'
irc_907.priority = 'high'


def irc_001 (cenni, input):
    cenni.is_connected = True
    return
irc_001.rule = r'(.*)'
irc_001.event = '001'
irc_001.priority = 'high'


def irc_cap_end (cenni, input):
    cenni.write(('CAP', 'END'))
    return


if __name__ == '__main__':
    print(__doc__.strip())
