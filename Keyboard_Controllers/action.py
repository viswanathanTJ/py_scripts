import warnings
warnings.filterwarnings("ignore")
import pytesseract
import clipboard
from PIL import Image
import pyautogui as pg
import os
import Quartz
from threading import Thread
from time import sleep
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

f, thread = False, None
def do_work(flag):
    while flag():
        pg.press('cmd')
        pg.moveRel(randint(-200, 200), randint(-200, 200))
        print(dt.now().strftime("%d-%m-%y %I:%M:%S %p"))
        sleep(50)

def alive():
    global f, thread
    f = not f
    if f:
        notify('Status', 'starting alive script')
        print('starting alive script')
        thread = Thread(target=do_work, args=(lambda: f,))
        thread.start()
    elif thread:
        notify('Status', 'stopping alive script')
        print('stopping alive script')
        thread.join()


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
