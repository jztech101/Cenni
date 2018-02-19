#!/usr/bin/env python3
import re, urllib2.request, urllib2.parse, urllib2.error
import web

definitions = 'https://github.com/myano/kenni/wiki/oblique'

r_item = re.compile(r'(?i)<li>(.*?)</li>')
r_tag = re.compile(r'<[^>]+>')

def mappings(uri):
    result = {}
    bytes = web.get(uri)
    for item in r_item.findall(bytes):
        item = r_tag.sub('', item).strip(' \t\r\n')
        if not ' ' in item: continue

        command, template = item.split(' ', 1)
        if not command.isalnum(): continue
        if not template.startswith(('http://', 'https://')): continue
        result[command] = template.replace('&amp;', '&')
    return result

def service(kenni, input, command, args):
    t = o.services[command]
    template = t.replace('${args}', urllib2.parse.quote(args.encode('utf-8'), ''))
    template = template.replace('${nick}', urllib2.parse.quote(input.nick, ''))
    uri = template.replace('${sender}', urllib2.parse.quote(input.sender, ''))

    info = web.head(uri)
    if isinstance(info, list):
        info = info[0]
    if not 'text/plain' in info.get('content-type', '').lower():
        return kenni.say("Sorry, the service didn't respond in plain text.")
    bytes = web.get(uri)
    lines = bytes.splitlines()
    if not lines:
        return kenni.say("Sorry, the service didn't respond any output.")
    try: line = lines[0].encode('utf-8')[:350]
    except: line = lines[0][:250]
    kenni.say(line)

def refresh(kenni):
    if hasattr(kenni.config, 'services'):
        services = kenni.config.services
    else: services = definitions

    old = o.services
    o.serviceURI = services
    o.services = mappings(o.serviceURI)
    return len(o.services), set(o.services) - set(old)

def o(kenni, input):
    """Call a webservice."""
    text = input.group(2)

    if (not o.services) or (text == 'refresh'):
        length, added = refresh(kenni)
        if text == 'refresh':
            msg = 'Okay, found %s services.' % length
            if added:
                msg += ' Added: ' + ', '.join(sorted(added)[:5])
                if len(added) > 5: msg += ', &c.'
            return kenni.say(msg)

    if not text:
        return kenni.say('Try %s for details.' % o.serviceURI)

    if ' ' in text:
        command, args = text.split(' ', 1)
    else: command, args = text, ''
    command = command.lower()

    if command == 'service':
        msg = o.services.get(args, 'No such service!')
        return kenni.say(msg)

    if command not in o.services:
        return kenni.say('Service not found in %s' % o.serviceURI)

    if hasattr(kenni.config, 'external'):
        default = kenni.config.external.get('*')
        manifest = kenni.config.external.get(input.sender, default)
        if manifest:
            commands = set(manifest)
            if (command not in commands) and (manifest[0] != '!'):
                return kenni.say('Sorry, %s is not whitelisted' % command)
            elif (command in commands) and (manifest[0] == '!'):
                return kenni.say('Sorry, %s is blacklisted' % command)
    service(kenni, input, command, args)
o.commands = ['o','oblique']
o.example = '.o servicename arg1 arg2 arg3'
o.services = {}
o.serviceURI = None
o.rate = 20

def snippet(kenni, input):
    if not o.services:
        refresh(kenni)

    search = urllib2.parse.quote(input.group(2).encode('utf-8'))
    py = "BeautifulSoup.BeautifulSoup(re.sub('<.*?>|(?<= ) +', '', " + \
          "''.join(chr(ord(c)) for c in " + \
          "eval(urllib2.urlopen('https://ajax.googleapis.com/ajax/serv" + \
          "ices/search/web?v=1.0&q=" + search + "').read()" + \
          ".replace('null', 'None'))['responseData']['resul" + \
          "ts'][0]['content'].decode('unicode-escape')).replace(" + \
          "'&quot;', '\x22')), convertEntities=True)"
    service(kenni, input, 'py', py)
snippet.commands = ['snippet']
snippet.rate = 20

if __name__ == '__main__':
    print(__doc__.strip())
