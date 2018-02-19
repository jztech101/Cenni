#!/usr/bin/env python3import sys, os, time, threading, signal
from . import bot

class Watcher(object):
    # Cf. http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496735
    def __init__(self):
        self.child = os.fork()
        if self.child != 0:
            self.watch()

    def watch(self):
        try: os.wait()
        except KeyboardInterrupt:
            self.kill()
        sys.exit()

    def kill(self):
        try: os.kill(self.child, signal.SIGKILL)
        except OSError: pass

def run_kenni(config):
    if hasattr(config, 'delay'):
        delay = config.delay
    else: delay = 20

    def connect(config):
        p = bot.kenni(config)
        p.use_ssl = config.ssl
        p.use_sasl = config.sasl
        p.run(config.host, config.port)

    try: Watcher()
    except Exception as e:
        print('Warning:', e, '(in __init__.py)', file=sys.stderr)

    while True:
        try: connect(config)
        except KeyboardInterrupt:
            sys.exit()

        if not isinstance(delay, int):
            break

        warning = 'Warning: Disconnected. Reconnecting in %s seconds...' % delay
        print(warning, file=sys.stderr)
        time.sleep(delay)

def run(config):
    t = threading.Thread(target=run_kenni, args=(config,))
    if hasattr(t, 'run'):
        t.run()
    else: t.start()

if __name__ == '__main__':
    print(__doc__)
