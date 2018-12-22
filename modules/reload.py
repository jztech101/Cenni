#!/usr/bin/env python3
import sys, os.path, time, imp
import irc

def f_reload(cenni, input):
    """Reloads a module, for use by admins only."""
    if not input.admin: return

    name = input.group(2)
    if name == cenni.config.owner:
        return cenni.say('What?')

    if (not name) or (name == '*'):
        cenni.variables = None
        cenni.commands = None
        cenni.setup()
#        if cenni.logchan_pm:
#            cenni.msg(cenni.logchan_pm, '[Reload] %s: [%s] Total' % (input.nick+ '!' + input.user + '@' + input.host, input.sender))
        return cenni.say('done')

    if name not in sys.modules:
        return cenni.say('%s: no such module!' % name)

    # Thanks to moot for prodding me on this
    path = sys.modules[name].__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return cenni.say('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'):
        module.setup(cenni)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    cenni.register(vars(module))
    cenni.bind_commands()

    cenni.say('%r (version: %s)' % (module, modified))
#    if cenni.logchan_pm:
#        cenni.msg(cenni.logchan_pm, '[Reload] %s: [%s] %r' % (input.nick+ '!' + input.user + '@' + input.host,input.sender, module))
f_reload.commands = ['reload']
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'
f_reload.thread = False

if __name__ == '__main__':
    print(__doc__.strip())
