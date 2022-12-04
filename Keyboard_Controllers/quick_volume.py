from pynput import keyboard
import osascript
import pyautogui as pg

def volume(isup):
    result = osascript.osascript('get volume settings')
    volInfo = result[1].split(',')
    outputVol = int(volInfo[0].replace('output volume:', ''))
    print(outputVol)
    osascript.osascript("set volume output volume {}".format(outputVol + 10 if isup else outputVol - 10))

def onpress(key):
    if key == keyboard.Key.esc:
        return False
    try:  k = key.char
    except: k = key.name
    if k == '\\':
        print(pg.position())
    if k == 'down' or k == 'ctrl':
        volume(False)
    elif k == 'up' or k == 'alt':
        volume(True)

print('Script started')

try:
    with keyboard.Listener(on_press=onpress) as l:
        l.join()
except KeyboardInterrupt:
    print('Byee')