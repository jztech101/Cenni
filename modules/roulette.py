#!/usr/bin/env python3# -*- coding: utf-8 -*-
import random
import tools
barrel = dict()
currentbarrel = dict()
def roulette(cenni, input):
    global barrel, currentbarrel
    if not tools.isChan(input.sender, False):
        return
    if hasattr(cenni.config, 'rouletteC') and input.sender in cenni.config.rouletteC:
        if not cenni.config.rouletteC[input.sender]:
            return
    else:
        return
    random.seed()
    if input.sender not in barrel or barrel[input.sender] == None or (input.group(2) and input.group(2).lower() == 'spin'):
        barrel[input.sender] = random.randint(1,8)
        currentbarrel[input.sender] = 1
        if input.group(2) and input.group(2).lower() == 'spin':
            return cenni.say("Feeling lucky?")
    if barrel[input.sender] == currentbarrel[input.sender]:
        if cenni.nick.lower() in cenni.ops[input.sender]:
            cenni.write(['KICK', input.sender, input.nick, "BANG"])
        else:
            cenni.write(['PRIVMSG', input.sender], "\x01ACTION kicks " + input.nick +"\x01")
        barrel[input.sender] = None
    else:
        cenni.say("*CLICK*")
        currentbarrel[input.sender] += 1
#        print(barrel[input.sender])
roulette.commands = ['rr','roulette']
roulette.priority= 'high'

if __name__ == '__main__':
    print(__doc__.strip())
