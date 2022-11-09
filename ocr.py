from pynput import keyboard
import pyautogui as pg
import clipboard
import pytesseract
import os
from PIL import Image

shortcut = ('ctrl', 'cmd') 
quitcut = ('ctrl', 'esc')

# Functions

def notify(title, message):
    os.system('osascript -e \'display notification "{}" with title "{}"\''.format(message, title))

selection = False
sx, sy = 0, 0
def scanner():
    global selection, sx, sy
    
    if not selection:
        sx, sy = pg.position()  
        print('Starting point noted', sx, sy)
        notify("OCR", "Starting point noted")
    else:
        x, y = pg.position()
        print('Ending point is', x, y)
        img = pg.screenshot()
        img = img.resize((1680,1000), Image.ANTIALIAS)
        img.save('org.png')
        img = img.crop((sx, sy, x, y))
        img.save('crop.png')

        text = pytesseract.image_to_string(img)
        print(text, "\n")
        clipboard.copy(text)
        notify("OCR", "Text copied to clipboard")

    selection = not selection
        
### Keyboard Actions    
pressed = set()
def getKey(key):
    try: return key.char
    except: return key.name

def onpress(key):
    k = getKey(key)
    if k in shortcut or k in quitcut:
        pressed.add(k)
    if all(q in pressed for q in quitcut):
        print("Exiting...")
        listener.stop()
    elif all(s in pressed for s in shortcut):
        scanner()
        
def onrelease(key):
    k = getKey(key)
    if k in shortcut or k in quitcut:
        pressed.remove(k)

with keyboard.Listener(on_press=onpress, on_release=onrelease) as listener:
    listener.join()
