#!/usr/bin/env python3
import re
import tools

def spamDetConfig(cenni, a):
    if hasattr(cenni.config, 'spamdet') and a in cenni.config.spamdet:
        if cenni.config.spamdet[a]:
            return True
    return False

def useRemove(cenni, a):
    if hasattr(cenni.config, 'useremove') and a in cenni.config.useremove:
        if cenni.config.useremove[a]:
            return True
    return False

def f_spamDet(cenni, input):
    text = input.group(1)
    if not tools.isChan(input.sender, True):
        return
    kickstr = "KICK"
    if useRemove(cenni,input.sender):
        kickstr="REMOVE"
    spamregexes = []
    spamkickmsg = []

    spamregexes.append('.*just posted this.*freenode blog')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('After the acquisition by Private Internet Access, Freenode is now being used')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('b(L|I)og (where|by) freenode staff member')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('freenode pedophilia scanda(l|I)')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('Read what (i|l)rc (i|l)nvest(l|i)gat(l|i)ve journa[l|i][l|i]sts')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('A fasc[i|l]nat[i|l]ng b[i|l]og where freenode staff')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('A(L|I)+ to(L|I)d, handshake a(L|I)ms to g(L|I)ve')
    spamkickmsg.append('Propoganda Spam')
    spamregexes.append('freenode is reg(I|L)stered.*by guarantee without')
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
    spamregexes.append('.*▄.*▄.*')
    spamkickmsg.append('Graffiti Spam')

    spamregexes.append(' {4,}')
    spamkickmsg.append('Line Spam')
    spamregexes.append('[A-Za-z0-9]{25,}')
    spamkickmsg.append('Line Spam')
    spamregexes.append('( [A-Za-z0-9]){4,}')
    spamkickmsg.append('Line Spam')

    msg2 = tools.removeFormatting(text)
    msg2 = tools.replaceUnicode(msg2)
    print("[Filter] " + msg2)
    nicks = 0
    if spamDetConfig(cenni, input.sender):
        for i in range(0, len(spamregexes)):
            if re.search(spamregexes[i],msg2, re.IGNORECASE):
                cenni.write([kickstr, input.sender, input.nick,' :', spamkickmsg[i]])
                if cenni.logchan_pm:
                    cenni.msg(cenni.logchan_pm, '['+spamkickmsg[i]+'] ' + input.nick + '!' + input.user + '@' + input.host +': ['+ input.sender +'] ' + msg2)
                return
        for i in msg2.split(" "):
            if i.lower() in cenni.users[input.sender]:
                 print(i)
                 nicks = nicks + 1
            if nicks >= 4:
                cenni.write([kickstr,input.sender, input.nick, " :Mass Highlight Spam"])
                if cenni.logchan_pm:
                    cenni.msg(cenni.logchan_pm, '[Mass Highlight Spam] ' + input.nick + '!' + input.user + '@' + input.host+': ['+input.sender+'] ' + msg2)
                return
f_spamDet.rule = r'(.*)'
f_spamDet.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())

