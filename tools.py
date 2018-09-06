#!/usr/bin/env python3
import re
def isChan(chan, checkprefix):
    if not chan:
        return False
    elif chan.startswith("#"):
        return True
    elif checkprefix and len(chan) >= 2 and not chan[0].isalnum() and chan[1] == "#":
        return True
    else:
        return False

def replaceUnicode(string):
    string = re.sub('[ᎳᏔ]','W',string)
    string = re.sub('[οⲟഠо]','o',string)
    string = re.sub('[һ]','h',string)
    string = re.sub('[ỿу]','y',string)
    string = re.sub('[ᥙ]','u',string)
    string = re.sub('[ⅠⅼΙ]','I',string)
    string = re.sub('[іⅰ]','i',string)
    string = re.sub('[ᖇᏒᎡ]','R',string)
    string = re.sub('[ϹС]','C',string)
    string = re.sub('[ⅽсϲ]','c',string)
    string = re.sub('[ѕ]','s',string)
    string = re.sub('[ᥱе]','e',string)
    string = re.sub('[АᎪΑ]','A',string)
    string = re.sub('[аɑ]','a',string)
    string = re.sub('[ⅿ]','m', string)
    string = re.sub('[ⅾԁ]','d',string)
    string = re.sub('[ᥒ]','n',string)
    string = re.sub('[ɡ]','g',string)
    string = re.sub('[рⲣ]','p', string)
    string = re.sub('[ᴠⅴ]','v', string)
    string = re.sub('[ϳ]','j',string)
    string = re.sub('[∪]','U', string)
    string = re.sub('[           ]',' ',string)
    return string

def removeFormatting(string):
    return re.sub('[\x02\x0F\x16\x1D\x1F]|\x03(\d{,2}(,\d{,2})?)?',' ',string)

