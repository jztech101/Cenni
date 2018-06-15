#!/usr/bin/env python3
import imp, os, sys

class Configs():
    def __init__(self, config_paths):
        self.config_paths = config_paths

    def load_modules(self, config_modules):
        for config_name in self.config_paths:
            name = os.path.basename(config_name).split('.')[0] + '_config'
            module = imp.load_source(name, config_name)
            module.filename = config_name

            if not hasattr(module, 'prefix'):
                module.prefix = r'\.'

            if not hasattr(module, 'name'):
                module.name = 'Cenni: https://github.com/jztech101/cenni/'

            if not hasattr(module, 'port'):
                module.port = 6667

            if not hasattr(module, 'password'):
                module.password = None

            if not hasattr(module, 'ssl'):
                module.ssl = False

            if module.host == 'irc.example.net':
                error = ('Error: you must edit the config file first!\n' +
                            "You're currently using %s" % module.filename)
                print(error, file=sys.stderr)
                sys.exit(1)

            config_modules.append(module)

