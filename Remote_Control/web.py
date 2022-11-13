import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import osascript
import os
import pyautogui as pg
import Quartz
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

hid = {'playpause': 16, 'next': 17, 'prev': 18, 'volup': 0, 'voldown': 1, 'forward': 19, 'backward': 20, 'brightup': 2, 'brightdown': 3}

def HIDPostAuxKey(key): 
    def doKey(down):
        ev = Quartz.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(14, (0,0), 0xa00 if down else 0xb00, 0, 0, 0, 8, (key << 16) | ((0xa if down else 0xb) << 8), -1)
        cev = ev.CGEvent()
        Quartz.CGEventPost(0, cev)
    doKey(True)
    doKey(False)
  
app = FastAPI(middleware=middleware)

templates = Jinja2Templates(directory=os.path.dirname(__file__))


@app.get('/')
def index(req: Request):
    return templates.TemplateResponse('index.html', {"request": req})

@app.get('/cmd/{cmd}')
def plus(cmd: str):
    match cmd:
        case cmd if cmd in hid: 
            HIDPostAuxKey(hid[cmd])
        case 'volUp': return volume(True)
        case 'volDown': return volume(False)
        case 'right': pg.press('right')
        case 'left': pg.press('left')
        case 'getVol': return getVol()


@app.get('/getIP')
def getIP():
    return {'ip':os.popen('ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2').read().strip()}
    
def getVol():
    result = osascript.osascript('get volume settings')
    volinfo = result[1].split(',')
    outputVol = int(volinfo[0].replace('output volume:',  ''))
    return outputVol

@app.get('/setVol/{level}')
def setVol(level):
    osascript.osascript('set volume output volume {}'.format(level))

def volume(isup):
    outputVol = getVol()
    newVol = outputVol + 10 if isup else outputVol - 10
    osascript.osascript("set volume output volume {}".format(newVol))
    return newVol

if __name__ == "__main__":
    uvicorn.run("web:app", host='0.0.0.0', port=80, reload=True)