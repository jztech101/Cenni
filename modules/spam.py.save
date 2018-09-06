#!/usr/bin/env python3
import re
import tools

def spamDet(cenni, a):
    if hasattr(cenni.config, 'spamdet') and a in cenni.config.spamdet:
        if cenni.config.spamdet[a]:
            return True
    return False

def useRemove(cenni, a):
    if hasattr(cenni.config, 'useremove') and a in cenni.config.useremove:
        if cenni.config.useremove[a]:
            return True
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

def f_spam(cenni, input):
    text = input.group(1)
    if not tools.isChan(input.sender, True):
        return
    kickstr = "KICK"
    if useRemove(cenni,input.sender):
        kickstr="REMOVE"
    spamregexes = []
    spamkickmsg = []
    spamregexes.append('.*▄.*▄.*')
    spamkickmsg.append('Spam Script')

    spamregexes.append('.*just posted this.*freenode blog')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('After the acquisition by Private Internet Access, Freenode is now being used')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('b(L|I)og (where|by) freenode staff member')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('freenode pedophilia scanda(l|I)')
    spamkickmsg.append('Propoganda Spam')

    spamregexes.append('with our irc ad service')
    spamkickmsg.append('Ad Spam')

    spamregexes.append('wqz')
    spamkickmsg.append('Link Spam')
    spamregexes.append('LRH')
    spamkickmsg.append('Link Spam')
    spamregexes.append('ADn2IJnTRyM')
    spamkickmsg.append('Link Spam')

    spamregexes.append('A[il]+ah [li]s do[li]ng')
    spamkickmsg.append('Religious Spam')
    spamregexes.append('(moon|sun) [li]s not do[li]ng')
    spamkickmsg.append('Religious Spam')
    spamregexes.append('(stars|p[li]anets|ga[li]ax[li]es|oceans) are not doing')
    spamkickmsg.append('Religious Spam')


    spamregexes.append('([^A-Za-z0-9 ]{2,}  ){2,}')
    spamkickmsg.append('Graffiti Spam')

    spamregexes.append(' {4,}')
    spamkickmsg.append('Line Spam')
    spamregexes.append('[A-Za-z0-9]{25,}')
    spamkickmsg.append('Line Spam')
    spamregexes.append('( [A-Za-z0-9]){4,}')
    spamkickmsg.append('Line Spam')

    msg2 = removeFormatting(text)
    msg2 = replaceUnicode(msg2)
    print("[Filter] " + msg2)
    nicks = 0
    if spamDet(cenni, input.sender):
        for i in range(0, len(spamregexes)):
            if re.search(spamregexes[i],msg2, re.IGNORECASE):
                cenni.write([kickstr, input.sender, input.nick,' :', spamkickmsg[i]])
                return
        for i in msg2.split(" "):
            print(i)
            if i.lower() in cenni.users[input.sender]:
                 print(i)
                 nicks = nicks + 1
            if nicks >= 4:
                cenni.write([kickstr,input.sender, input.nick, " :Mass Highlight Spam"])
                return
f_spam.rule = r'(.*)'
f_spam.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())

