#!/usr/bin/env python3
import re
import web

whyuri = 'http://www.leonatkinson.com/random/index.php/rest.html?method=advice'
r_paragraph = re.compile(r'<quote>.*?</quote>')


def getwhy(kenni, input):
    page = web.get(whyuri)
    paragraphs = r_paragraph.findall(page.decode('utf-8'))
    out = str()
    if paragraphs:
        line = re.sub(r'<[^>]*?>', '', str(paragraphs[0]))
        out = line.lower().capitalize() + "."
    else:
        out = 'We are unable to find any reasons *why* this should work.'

    return kenni.say(out)
getwhy.commands = ['why', 'tubbs']
getwhy.thread = False
getwhy.rate = 30

if __name__ == '__main__':
    print(__doc__.strip())
