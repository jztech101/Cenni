#!/usr/bin/env python3
import re
import urllib
from html.entities import name2codepoint
from modules import unicode as uc
import urllib.request
import sys

r_entity = re.compile(r'&([^;\s]+);')


class Grab(urllib.request.URLopener):
    def __init__(self, *args):
        self.version = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        urllib.request.URLopener.__init__(self, *args)

    def http_error_default(self, url, fp, errcode, errmsg, headers):
        return urllib.addinfourl(fp, [headers, errcode], "http:" + url)
urllib.request._urlopener = Grab()

def get(uri):
    if not uri.startswith('http'):
        return
    req = urllib.request.Request(uri, headers={'Accept':'*/*'})
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
    u = urllib.request.urlopen(req)
    bytes = u.read()
    u.close()
    return bytes


def head(uri):
    if not uri.startswith('http'):
        return
    u = urllib.request.urlopen(uri)
    info = u.info()
    u.close()
    return info


def head_info(uri):
    if not uri.startswith('http'):
        return
    output = dict()

    u = urllib.request.urlopen(uri)
    if hasattr(u, 'geturl'):
        output['geturl'] = u.geturl()
    if hasattr(u, 'code'):
        output['code'] = u.code
    if hasattr(u, 'url'):
        output['url'] = u.url
    if hasattr(u, 'headers'):
        output['headers'] = u.headers
    if hasattr(u, 'info'):
        output['info'] = u.info()

    u.close()
    return output


def post(uri, query):
    if not uri.startswith('http'):
        return
    data = urllib.parse.urlencode(query)
    u = urllib.request.urlopen(uri, data)
    bytes = u.read()
    u.close()
    return bytes



def entity(match):
    value = match.group(1).lower()
    if value.startswith('#x'):
        return chr(int(value[2:], 16))
    elif value.startswith('#'):
        return chr(int(value[1:]))
    elif value in name2codepoint:
        return chr(name2codepoint[value])
    return '[' + value + ']'


def decode(html):
    return r_entity.sub(entity, html)

def entity_replace(txt):
    return r_entity.sub(ep, txt)

def ep(m):
    entity = m.group()
    if entity.startswith('&#x'):
        cp = int(entity[3:-1], 16)
        meep = chr(cp)
    elif entity.startswith('&#'):
        cp = int(entity[2:-1])
        meep = chr(cp)
    else:
        entity_stripped = entity[1:-1]
        try:
            char = name2codepoint[entity_stripped]
            meep = chr(char)
        except:
            if entity_stripped in HTML_ENTITIES:
                meep = HTML_ENTITIES[entity_stripped]
            else:
                meep = str()
    try:
        return uc.decode(meep)
    except:
        return uc.decode(uc.encode(meep))


def remove_xml_tags(txt):
    r_tag = re.compile(r'<(?!!)[^>]+>')
    return re.sub(r_tag, '', txt)


def get_urllib_object(uri, timeout):
    '''Return a urllib2 object for `uri` and `timeout`. This is better than
    using urrlib2 directly, for it handles redirects, makes sure URI is utf8,
    and is shorter and easier to use.
    Modules may use this if they need a urllib2 object to execute .read() on.
    For more information, refer to the urllib2 documentation.'''
    redirects = 0
    try:
        uri = uri.encode("utf-8")
    except:
        pass
    while True:
        req = urllib.request.Request(uri, headers={'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (cenni)'})
        try:
            u = urllib.request.urlopen(req, None, timeout)
        except urllib.error.HTTPError as e:
            return e.fp
        except:
            raise
        info = u.info()
        if not isinstance(info, list):
            status = '200'
        else:
            status = str(info[1])
            try: info = info[0]
            except: pass
        if status.startswith('3'):
            uri = urlparse.urljoin(uri, info['Location'])
        else: break
        redirects += 1
        if redirects >= 50:
            return "Too many re-directs."
    return u


def quote(string):
    '''Identical to urllib2.quote. Use this if you already importing web in
    your module and don't want to import urllib2 just to use the quote
    function.'''
    return urllib.parse.quote(string)


def urlencode(data):
    '''Identical to urllib.urlencode. Use this if you already importing web
    in your module and don't want to import urllib just to use the urlencode
    function.'''
    return urllib.parse.urlencode(data)


if __name__ == "__main__":
    main()
