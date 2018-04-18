#! python3
# Imgur Downlaoder.py - Downloads new images from favourite subs

import requests
import os
import bs4
import textme
import time

y = 1
num = 0


def imgursearch(arg, page=1):
    global imgUrl
    global num
    global y
    if arg.startswith('r/'):
        arg2 = arg[2:]
    else:
        arg2 = arg
    search = arg
    os.chdir(r'd:\downloads\python')
    for pg in range(page):
        # starting url
        url = f'http://imgur.com/r/{search}/page/{pg}'
        os.makedirs('imgur\\' + arg2, exist_ok=True)   # store in ./imgur
        print(f'Downloading page {url}...')

        '''requests'''
        res = requests.get(url)
        res.raise_for_status()

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        linkElems = soup.select('a[class="image-list-link"]')
        for i in range(len(linkElems)):
            # time.sleep(.5)
            # Download the page.
            try:
                res = requests.get('http://imgur.com' +
                                   linkElems[i].get('href'))
                res.raise_for_status()
            except IndexError:
                print('no image')
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            # Find the URL of the image.

            imgElem = soup.select('img.post-image-placeholder')

            '''beautiful soup'''
            for x in range(len(imgElem)):
                num += 1
                try:
                    imgUrl = 'http:' + imgElem[x].get('src')
                except IndexError:
                    print(f'Image {num} out of range.')
                    continue
                if os.path.exists(os.path.join('imgur\\' + arg2, arg2 + '_' + os.path.basename(imgUrl))):
                    print(f'Image {num} already exists.')
                    break
                if os.path.exists(os.path.join('imgur\\' + arg2, arg2 + '_' + os.path.basename(imgUrl)[:2])):
                    print(f'Image {num} already exists.')
                    break
                # Download the image.
                '''requests'''
                try:
                    print('Downloading image %s' %
                          (imgUrl) + ' from ' + arg + '...')
                    res = requests.get(imgUrl)
                    res.raise_for_status()
                except NameError:
                    print('Couldn\'t find name for download')
                # Save the image to ./imgur.
                try:
                    imageFile = open(os.path.join(
                        'imgur\\' + arg2, arg2 + '_' + os.path.basename(imgUrl)), 'wb')
                    for chunk in res.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
                    print(f'Image {num} saved! Total images saved: {y}')
                    y += 1
                except NameError:
                    print('no name for download')
                except OSError:
                    imageFile = open(os.path.join(
                        'imgur\\' + arg2, arg2 + '_' + os.path.basename(imgUrl)[:-2]), 'wb')
                    for chunk in res.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
                    print(f'Image {num} saved! Total images saved: {y}')
                    y += 1

    print(f'Done. Total images saved: {y}')


imgursearch('', 5)
