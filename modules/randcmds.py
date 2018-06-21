#!/usr/bin/env python3# -*- coding: utf-8 -*-
from random import randint
def potato(cenni, input):
    cenni.write(['PRIVMSG', input.sender], '\x01ACTION is a potato\x01')
potato.commands = ['potato']
potato.priority = 'high'
def moo(cenni, input):
    cenni.say('MoooooOoooOooooooooooo')
moo.commands = ['moo']
moo.priority = 'high'
def cookie(cenni, input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.write(['PRIVMSG', input.sender], '\x01ACTION gives ' + nick + ' a cookie\x01')
cookie.commands = ['cookie']
cookie.priority = 'high'
def source(cenni, input):
    cenni.say('Cenni: https://github.com/jztech101/cenni')
source.commands = ['source']
source.priority = 'high'
def shrug(cenni, input):
    cenni.say('┻━┻ ︵ ¯\_(ツ)_/¯ ︵ ┻━┻')
shrug.commands = ['shrug']
shrug.priority = 'high'
def hmmm(cenni, input):
    cenni.say('t' + u'\u200b' + 'est')
#    cenni.say(cenni.hostmasks["JZTech101"])
hmmm.commands = ['hmmm']
hmmm.priority = 'high'
def burn(cenni, input):
    cenni.write(['PRIVMSG', input.sender], '\x01ACTION watches the world burn\x01')
burn.commands = ['burn']
burn.priority = 'high'
if __name__ == '__main__':
    print(__doc__.strip())
