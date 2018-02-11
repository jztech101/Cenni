#!/usr/bin/env python2
'''
ask.py - kenni's Ask Module
Copyright 2011-2013, Michael Yanovich (yanovich.net)
Licensed under the Eiffel Forum License 2.

More info:
* Kenni: https://github.com/JZTech101/Kenni
* jenni: https://github.com/myano/jenni/ 
* Phenny: http://inamidst.com/phenny/
'''

import random, time

random.seed()

def ask(kenni, input):
    '''.ask <item1> or <item2> or <item3> - Randomly picks from a set of items seperated by ' or '.'''

    choices = input.group(2)

    if choices == None:
        kenni.say('There is no spoon! Please try a valid question.')
    elif choices.lower() == 'what is the answer to life, the universe, and everything?':
        ## cf. https://is.gd/2KYchV
        kenni.say('42')
    else:
        list_choices = choices.lower().split(' or ')
        if len(list_choices) == 1:
            ## if multiple things aren't listed
            ## default to yes/no
            kenni.say(random.choice(['yes', 'no']))
        else:
            ## randomly pick an item if multiple things
            ## are listed
            kenni.say((random.choice(list_choices)).encode('utf-8'))
ask.commands = ['ask']
ask.priority = 'low'
ask.example = '.ask today or tomorrow or next week'

if __name__ == '__main__':
    print __doc__.strip()
