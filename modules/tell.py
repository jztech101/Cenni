#!/usr/bin/env python3
import os, re, time, random
import threading
import tools


maximum = 4


def loadReminders(fn, lock):
    lock.acquire()
    try:
        result = {}
        f = open(fn)
        for line in f:
            line = line.strip()
            if line:
                try: tellee, teller, verb, timenow, msg = line.split('\t', 4)
                except ValueError: continue  # @@ hmm
                result.setdefault(tellee, []).append((teller, verb, timenow, msg))
        f.close()
    finally:
        lock.release()
    return result


def dumpReminders(fn, data, lock):
    lock.acquire()
    try:
        f = open(fn, 'w')
        for tellee in data.keys():
            for remindon in data[tellee]:
                line = '\t'.join((tellee,) + remindon)
                try: f.write(line + '\n')
                except IOError: break
        try: f.close()
        except IOError: pass
    finally:
        lock.release()
    return True


def setup(self):
    fn = self.nick + '-' + self.config.host + '.tell.db'
    self.tell_filename = os.path.join(os.path.expanduser('config'), fn)
    if not os.path.exists(self.tell_filename):
        try: f = open(self.tell_filename, 'w')
        except OSError: pass
        else:
            f.write('')
            f.close()
    self.tell_lock = threading.Lock()
    self.reminders = loadReminders(self.tell_filename, self.tell_lock)  # @@ tell


def f_remind(cenni, input):
    teller = input.nick

    #if hasattr(cenni.config, 'logchan_pm'):
        #cenni.msg(cenni.config.logchan_pm, 'TELL used by %s in %s: %s' % (str(input.nick), str(input.sender), input))

    #if not input.group(2) or input.group(3):
    if not input.group(2):
        return cenni.say('Please tell me who and what to tell people.')

    # @@ Multiple comma-separated tellees? Cf. Terje, #swhack, 2006-04-15
    line_prefix = (input.group()).lower()
    if input.group() and (re.match('^[^a-zA-Z]tell.*',line_prefix) or re.match('^[^a-zA-Z]yell.*',line_prefix)):
        verb = 'tell'.encode('utf-8')
        line = input.groups()
        line_txt = line[1].split()
        tellnick = line_txt[0].lower()
        tellee = line_txt[0].lower()
        msg = ' '.join(line_txt[1:])
        if re.match('^[^a-zA-Z]yell.*',line_prefix):
            msg = (msg).upper()
    else:
        verb, tellee, msg = input.groups()
    if not msg:
        cenni.say("Message cannot be empty")
        return
    ## handle unicode
    verb = verb.decode('utf-8')
    tellee = tellee.encode('utf-8').decode('utf-8')
    msg = msg.encode('utf-8').decode('utf-8')

    tellee = tellee.rstrip('.,:;')

    if not os.path.exists(cenni.tell_filename):
        return

    timenow = time.strftime('%d %b %H:%MZ', time.gmtime())
    whogets = list()
    response = list()
    for tellee in tellee.split(','):
        if len(tellee) > 20:
            response.append('Nickname %s is too long.' % (tellee))
            continue
        if tellee.lower() == cenni.nick.lower() or tellee.lower() == input.nick.lower():
            response.append("Cannot send to " + tellee)
            continue
        if tellee.lower() in cenni.accounts and cenni.accounts[tellee.lower()] != '0':
            tellee = cenni.accounts[tellee.lower()]
        elif tellee.lower() in cenni.hostmasks:
            tellee = cenni.idents[tellee.lower()]+ "@" +cenni.hostmasks[tellee.lower()]
        else:
            response.append(tellee + " not found")
            continue  # @@
        cenni.tell_lock.acquire()
        try:
            if not tellee in whogets:
                whogets.append(tellee)
                if tellee not in cenni.reminders:
                    cenni.reminders[tellee] = [(teller, verb, timenow, msg)]
                else:
                    cenni.reminders[tellee].append((teller, verb, timenow, msg))
        finally:
            cenni.tell_lock.release()
    if whogets:
        # print(", ".join(whogets))
        response.append("I'll pass that on when they're around")
    if response:
        cenni.say(", ".join(response))

    dumpReminders(cenni.tell_filename, cenni.reminders, cenni.tell_lock) # @@ tell
f_remind.rule = ('$nick', ['[tTyY]ell', '[aA]sk'], r'(\S+) (.*)')
f_remind.commands = ['tell', 'to', 'yell']


def getReminders(cenni, channel, key, tellee):
    lines = []
    template = '%s <%s> %s'
    today = time.strftime('%d %b', time.gmtime())

    cenni.tell_lock.acquire()

    try:
        for (teller, verb, datetime, msg) in cenni.reminders[key]:
            if datetime.startswith(today):
                datetime = datetime[len(today) + 1:]
            lines.append(template % (datetime, teller, msg))

        try: del cenni.reminders[key]
        except KeyError: cenni.msg(channel, 'Er...')
    finally:
        cenni.tell_lock.release()

    return lines


def message(cenni, input):
    #if not tools.isChan(input.sender, False): return

    tellee = input.nick.lower()
    channel = input.sender

    if not os: return
    if not os.path.exists(cenni.tell_filename):
        return
    if tellee in cenni.accounts and cenni.accounts[tellee] != '0':
        tellee = cenni.accounts[tellee]
    else:
        tellee = cenni.idents[tellee] + "@" +cenni.hostmasks[tellee]
    reminders = []
    remkeys = list(reversed(sorted(cenni.reminders.keys())))
    for remkey in remkeys:
        if not remkey.endswith('*') or remkey.endswith(':'):
            if tellee.lower() == remkey.lower():
                reminders.extend(getReminders(cenni, channel, remkey, tellee))
        elif tellee.lower().startswith(remkey.rstrip('*:').lower()):
            reminders.extend(getReminders(cenni, channel, remkey, tellee))
    if reminders:
        cenni.say(input.nick + ": Someone sent you a message while you were away! Please check PMs")
        for line in reminders:
            cenni.msg(input.nick, line)

    if len(list(cenni.reminders.keys())) != remkeys:
        dumpReminders(cenni.tell_filename, cenni.reminders, cenni.tell_lock)  # @@ tell
message.rule = r'(.*)'
message.priority = 'low'

if __name__ == '__main__':
    print(__doc__.strip())
