#!/usr/bin/env python3
import json
import random
import web
import re
from modules import unicode as uc

'''
Randall Munroe is nice and provides a simple JSON API for fetching comics.

See this page:
https://xkcd.com/json.html


Can access:
https://xkcd.com/info.0.json
for the current comic, or:
https://xkcd.com/614/info.0.json
for the 614th comic.

Each comic contains the following JSON keys:

{
 "month": "10"
,"num": 1432
, "link": ""
, "year": "2014"
, "news": ""
, "safe_title": "The Sake of Argument"
, "transcript": ""
, "alt": "'It's not actually ... it's a DEVICE for EXPLORING a PLAUSIBLE REALITY that's not the one we're in, to gain a broader understanding about it.' 'oh, like a boat!' '...' 'Just for the sake of argument, we should get a boat! You can invite the Devil, too, if you want.'"
, "img": "http:\/\/imgs.xkcd.com\/comics\/the_sake_of_argument.png"
, "title": "The Sake of Argument"
, "day": "10"
}

'''

random.seed()


def xkcd(kenni, input):
    '''.xkcd - Print all available information about the most recent (or specified) XKCD clip.'''

    def tryToGetJSON (site_url):
        try:
            page = web.get(xkcd_url)
        except:
            return kenni.say('Failed to access xkcd.com: <' + xkcd_url + '>')
        try:
            body = json.loads(page)
        except:
            return kenni.say('Failed to make use of data loaded by xkcd.com: <' + xkcd_url + '>')
        return body


    xkcd_url = 'https://xkcd.com/info.0.json'

    show_random_comic = False

    line = input.group(2)
    if line:
        if line.isdigit():
            xkcd_num = line.lstrip().rstrip()
            xkcd_url = 'https://xkcd.com/' + xkcd_num + '/info.0.json'
        elif any([line.lower() in ['r', 'ran', 'rand', 'random']]):
            show_random_comic = True
        else:
            kenni.say('Incorrect argument for .xkcd: ' + line)


    body = tryToGetJSON(xkcd_url)

    if show_random_comic:
        max_int = body['num']
        xkcd_rand_num = random.randint(0, max_int)
        xkcd_url = 'https://xkcd.com/' + str(xkcd_rand_num) + '/info.0.json'
        body = tryToGetJSON(xkcd_url)


    comic_date_str = body['year'] + '-' + str(body['month']).zfill(2) + '-' + str(body['day']).zfill(2)
    header_str = '\x02xkcd #\x02' + str(body['num']) + ' (' + comic_date_str + ') \x02' + body['title'] + '\x02'
    kenni.say(header_str)

    if body['transcript'].encode('UTF-8'):
        transcript_text = '\x02Transcript:\x02 ' + body['transcript']
        kenni.say(transcript_text)


    alt_text = '\x02Alt text\x02: ' + body['alt']
    kenni.say(alt_text)

    img_ssl_link = '[ ' + re.sub(r'http://', 'https://ssl', body['img']) + ' ]'
    kenni.say(img_ssl_link)


xkcd.commands = ['xkcd']
xkcd.example = '.xkcd  (for most recent), .xkcd [comic number]  (for specific comic), or .xkcd [r | ran | rand | random]  (for a random comic)'
xkcd.priority = 'medium'

if __name__ == '__main__':
    print(__doc__.strip())
