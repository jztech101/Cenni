#!/usr/bin/env python3# coding=utf-8
import json
import re
import socket
import web
from modules import unicode as uc


base = 'http://ip-api.com/json/'
re_ip = re.compile('(?i)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
re_country = re.compile('(?i)(.+), (.+ of)')

def ip_lookup(cenni, input):
    txt = input.group(2)
    if not txt:
        return cenni.say("No search term!")
    response = "[IP/Host Lookup] "
    try:
        page = web.get(base + txt)
    except IOError as err:
        return cenni.say('Could not access given address. (Detailed error: %s)' % (err))
    try:
        results = json.loads(page.decode('utf-8'))
    except:
        return cenni.say('Did not receive proper JSON from %s' % (base))
    if results:
        response += txt
        spacing = ' |'
        for param in results:
            if not results[param]:
                results[param] = 'N/A'
        if 'query' in results:
            response += '%s Query: %s' %(spacing, results['query'])
        if 'city' in results:
            response += '%s City: %s' % (spacing, results['city'])
        if 'regionName' in results:
            response += '%s State: %s' % (spacing, results['regionName'])
        if 'country' in results:
            country = results['country']
            match = re_country.match(country)
            if match:
                country = ' '.join(reversed(match.groups()))
            response += '%s Country: %s' % (spacing, country)
        if 'timezone' in results:
            response += '%s Time Zone: %s' % (spacing, results['timezone'])
        if 'as' in results:
            response += '%s AS: %s' % (spacing, results['as'])
        if  'isp' in results:
            response += '%s ISP: %s' % (spacing, results['isp'])
    cenni.say(response)
ip_lookup.commands = ['ip','geoip', 'iplookup']
ip_lookup.example = ".iplookup 8.8.8.8"

def host(cenni, input):
    if input.group(2) in cenni.hostmasks:
        cenni.say(input.group(2) + "!" + cenni.idents[input.group(2)] + "@" + cenni.hostmasks[input.group(2)])
    else:
        cenni.say("No hostmask found")
host.commands = ['host', 'hostmask']
host.example = "host nick"

def who(cenni, input):
    if input.group(2) in cenni.accounts and cenni.accounts[input.group(2)] != 0:
       cenni.say(cenni.accounts[input.group(2)])
    else:
       cenni.say("No account found")
who.commands = ['who']
who.example = 'who'
def server(cenni, input):
    if input.group(2) in cenni.servers:
       cenni.say(cenni.servers[input.group(2)])
    else:
       cenni.say("No server found")
server.commands = ['server']
server.example = 'server'
def realname(cenni, input):
    if input.group(2) in cenni.realnames:
       cenni.say(cenni.realnames[input.group(2)])
    else:
       cenni.say("No real name found")
realname.commands = ['realname']
realname.example = 'realname'
def checkip(cenni,input):
    if input.group(2) in cenni.ips:
       cenni.say(cenni.ips[input.group(2)])
    else:
       cenni.say("No IP Found")
who.commands = ['checkip']
who.example = 'checkip'
if __name__ == '__main__':
    print(__doc__.strip())
