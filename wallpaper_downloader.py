import requests
from bs4 import BeautifulSoup
import os
import re
import time
import threading

# => To get url goto https://wall.alphacoders.com and enter search text then copy url
''' Enter details here and execute '''
url = 'https://wall.alphacoders.com/by_sub_category.php?id=193061&name=Programming+Wallpapers'
path = 'Wallpapers/Programmers'
''' *** *** *** *** '''

imgs = set(os.listdir())

def get():
    global count
    page = 1
    while True:
        html = requests.get(url+str(page)).text
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('a', href=re.compile('big'))
        threads = set()
        count += len(tags)
        print('Got', count, 'images')
        if len(tags) == 0:
            print('End page is', page)
            print('==> Total images got', count)
            break
        for t in tags:
            thread = threading.Thread(target=down_img, args=(domain+t.get('href'),))
            threads.add(thread)

        page += 1

        for thread in threads:
            thread.start()
            
            
def down_img(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img', {'class':'main-content'}).get('src')
    imr = requests.get(img, stream=True)
    file = img.split('/')[-1]
    if file not in imgs:
        imgs.add(file)
        if imr.status_code == 200:
            with open(file, 'wb') as f:
                for chunk in imr:
                    f.write(chunk)

        
if __name__ == "__main__":
    print('*** Script started ***')
    gstart = time.time()
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    domain = 'https://wall.alphacoders.com/'
    url += '&page='
    count = 0
    get()
    print('*** Script ended in', time.time() - gstart, '***')
    