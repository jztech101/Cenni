#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc

def getHost(cenni, nick):
    if nick.lower() in cenni.hostmasks:
        return nick + "!" + cenni.idents[nick.lower()] + "@" + cenni.hostmasks[nick.lower()]
    else:
        return "No hostmask found"

def host(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getHost(cenni,nick))
host.commands = ['host', 'hostmask']
host.example = "host nick"

def getAccount(cenni, nick):
    nick = nick.lower()
    if nick in cenni.accounts and cenni.accounts[nick] != 0:
       return "Account: " + cenni.accounts[nick]
    else:
       return "No account found"

def account(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getAccount(cenni,nick))
account.commands = ['acct','account']
account.example = 'account'

def getServer(cenni, nick):
    nick = nick.lower()
    if nick in cenni.servers:
       return nick+ " is connected to: " + cenni.servers[nick]
    else:
       return "No server found"

def server(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getServer(cenni,nick))
server.commands = ['server']
server.example = 'server'

def getRealname(cenni, nick):
    nick = nick.lower()
    if nick in cenni.realnames:
       return "Real Name: " + cenni.realnames[nick]
    else:
       return "No real name found"

def realname(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getRealname(cenni,nick))
realname.commands = ['realname']
realname.example = 'realname'

def getIP(cenni,nick):
    nick = nick.lower()
    if nick in cenni.ipaddrs and cenni.ipaddrs[nick] != '255.255.255.255':
       return "IP: " + cenni.ipaddrs[nick]
    else:
       return "No IP Found"

def checkip(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getIP(cenni,nick))
checkip.commands = ['checkip','getip']
checkip.example = 'checkip'

def who(cenni,input):
    nick = input.nick
    if input.group(2):
        nick = input.group(2)
    cenni.say(getHost(cenni,nick) + " || " + getIP(cenni,nick) + " || " + getRealname(cenni,nick) + " || " + getAccount(cenni,nick) + " || " + getServer(cenni,nick))
who.commands = ['who','whox']
who.example = 'who'

if __name__ == '__main__':
    print(__doc__.strip())
