import warnings
warnings.filterwarnings("ignore")
import pytesseract
import clipboard
from PIL import Image
import pyautogui as pg
import os
import Quartz
from threading import Timer
from random import randint
from datetime import datetime as dt

# HARDWARE KEY PRESS

def HIDPostAuxKey(key): 
    cmds = {'space': 16, 'right': 17, 'left': 18, 'up': 0, 'down': 1}
    key = cmds[key]
    def doKey(down):
        ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(14, (0,0), 0xa00 if down else 0xb00, 0, 0, 0, 8, (key << 16) | ((0xa if down else 0xb) << 8), -1)
        cev = ev.CGEvent()
        Quartz.CGEventPost(0, cev)
    doKey(True)
    doKey(False)


# MISC

def notify(title, message):
    os.system('osascript -e \'display notification "{}" with title "{}"\''.format(message, title))

run = False
flag = True
def do_work():
    if run:
        pg.press('cmd')
        pg.moveRel(randint(-200, 200), randint(-200, 200))
        print(dt.now().strftime("%d-%m-%y %I:%M:%S %p"))
        Timer(3.0, do_work).start()

def alive():
    global flag, run
    if flag:
        run = True
        notify('Status', 'starting alive script')
        do_work()
    else:
        run = False
        notify('Status', 'stopping alive script')
    flag = not flag

# OCR

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
        img = img.resize((1650,1000), Image.ANTIALIAS)
        img.save('org.png')
        try:
            img = img.crop((sx, sy, x, y))
        except:
            print('Coordinates error')
        img.save('crop.png')

        text = pytesseract.image_to_string(img)
        print(text, "\n")
        clipboard.copy(text)
        notify("OCR", "Text copied to clipboard")

    selection = not selection
