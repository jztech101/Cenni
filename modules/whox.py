#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc

def host(cenni, input):
    if input.group(2) in cenni.hostmasks:
        cenni.say(input.group(2) + "!" + cenni.idents[input.group(2)] + "@" + cenni.hostmasks[input.group(2)])
    else:
        cenni.say("No hostmask found")
host.commands = ['host', 'hostmask']
host.example = "host nick"

def account(cenni, input):
    nick = input.group(2).lower()
    if nick in cenni.accounts and cenni.accounts[nick] != 0:
       cenni.say("Account: " + cenni.accounts[nick])
    else:
       cenni.say("No account found")
account.commands = ['acct','account']
account.example = 'account'
def server(cenni, input):
    nick = input.group(2).lower()
    if nick in cenni.servers:
       cenni.say(input.group(2)+ " is connected to: " + cenni.servers[nick])
    else:
       cenni.say("No server found")
server.commands = ['server']
server.example = 'server'
def realname(cenni, input):
    nick = input.group(2).lower()
    if nick in cenni.realnames:
       cenni.say("Real Name: " + cenni.realnames[nick])
    else:
       cenni.say("No real name found")
realname.commands = ['realname']
realname.example = 'realname'
def checkip(cenni,input):
    nick = input.group(2).lower()
    if nick in cenni.ipaddrs and cenni.ipaddrs[nick] != '255.255.255.255':
       cenni.say("IP: " + cenni.ipaddrs[nick])
    else:
       cenni.say("No IP Found")
checkip.commands = ['checkip','getip']
checkip.example = 'checkip'
if __name__ == '__main__':
    print(__doc__.strip())
