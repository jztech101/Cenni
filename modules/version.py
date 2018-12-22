#!/usr/bin/env python3
from datetime import datetime
from subprocess import *
import sys


def git_info():
    p = Popen(['git', 'log', '-n 1'], stdout=PIPE, close_fds=True)

    commit = p.stdout.readline().decode("utf-8")
    author = p.stdout.readline().decode("utf-8")
    date = p.stdout.readline().decode("utf-8")
    return commit + " " +  author + " " + date


def version(cenni, input):

    cenni.say("Cenni on Python " + sys.version)
version.commands = ['version']
version.priority = 'medium'
version.rate = 10


if __name__ == '__main__':
    print(__doc__.strip())
