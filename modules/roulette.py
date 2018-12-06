#!/usr/bin/env python3# -*- coding: utf-8 -*-
import random
import tools
def roulette(cenni, input):
    if not tools.isChan(input.sender, False):
        return
    random.seed()
    randnum = random.randint(1,3)
    if randnum == 2:
        if cenni.nick.lower() in cenni.ops[input.sender]:
            cenni.write(['KICK', input.sender, input.nick, "BANG"])
        else:
            cenni.write(['PRIVMSG', input.sender], "\x01ACTION kicks " + input.nick +"\x01")
    else:
        cenni.say("*CLICK*")
roulette.commands = ['rr','roulette']
roulette.priority= 'high'

if __name__ == '__main__':
    print(__doc__.strip())
