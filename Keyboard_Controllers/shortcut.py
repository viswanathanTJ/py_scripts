from pynput.keyboard import Listener
from action import *


shortcuts = {
    'ctrl,cmd': scanner,
    '/,alt': alive
    }

hotkeys = {'/'}
[hotkeys.add(e) for s in shortcuts.keys() for e in s.split(',') ]
pressed = set()

def get_key(key):
    try: return key.char
    except: return key.name

def onpress(key):
    global state
    k = get_key(key)
    if '/' in pressed and k == 'tab': 
        notify('Automator', '*** Stopping shortcuts script ***')
        return False
    if k in hotkeys: pressed.add(k)
    # for Hardware keys
    if '/' in pressed and k in cmds.keys(): 
        HIDPostAuxKey(k)
        return True
    # for all functions
    for shortcut, fun in shortcuts.items():
        if all(e in pressed for e in shortcut.split(',')):
            fun()

def onrelease(key):
    k = get_key(key)
    if k in pressed: pressed.remove(k)

try:
    with Listener(on_press=onpress, on_release=onrelease) as listener:
        print('*** Shortcuts scrips activated ***')
        notify('Automator', '*** Shortcuts scrips activated ***')
        listener.join()
except KeyboardInterrupt:
    print('*** Shortcuts scrips deactivated ***')
