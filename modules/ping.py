#!/usr/bin/env python3
import random

def f_ping(cenni, input):
    """ping cenni in a channel or pm"""
    cenni.say('pong')
f_ping.commands = ['ping']
f_ping.priority = 'high'

def f_pong(cenni, input):
    cenni.say('ping')
f_pong.commands = ['pong']
f_pong.priority = 'high'

if __name__ == '__main__':
    print(__doc__.strip())

