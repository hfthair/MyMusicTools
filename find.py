import os
import json
import random
import time
import requests
import ytm

api = ytm.YouTubeMusic()

repl = str.maketrans(
    "áéúíóàèìòù",
    "aeuioaeuio"
)


def escape(x):
    x = x.replace('&', '').replace('?', '').replace('=', '').replace('#', '')
    return x.translate(repl).lower().strip()


def format(found):
    return f'{found["title"]}({found["artists"]})<{found["source"]}>'


def find(src, progress):
    for title, artists in src:
        title = escape(title)
        artist = escape(artists.split(';')[0])
        key = f'{title}({artist})'

        print(f' # {title}({artist})\t', end='')
        if key in progress:
            print(' [already done] ==>', format(progress[key]))
            continue

        r = None
        try:
            r = find_ytm(title, artist)
        except:
            print(' exception search ytm.')
        if not r:
            try:
                r = find_migu(title, artist)
            except:
                print(' exception search migu.')
        if r:
            print(' ==>', format(r))
            progress[key] = r
        else:
            print(' ==> not found')
    return progress


def find_ytm(title, artist):
    time.sleep(random.random() + 0.3)
    title = title.lower()
    artist = artist.lower()

    r = api.search(title)
    r = [{
        'title': escape(i['name']),
        'artists': escape(';'.join([j['name'] for j in i['artists']])),
        'url': f'https://music.youtube.com/watch?v={i["id"]}',
        'source': 'ytm'
    } for i in r['songs']]

    match = [i for i in r if title == i['title'] and artist == i['artists']]
    if not match:
        match = [i for i in r if title in i['title']
                 and artist in i['artists']]
    if not match:
        match = [i for i in r if title == i['title']]
    if not match:
        match = [i for i in r if i['title'].startswith(title) or title.startswith(i['title'])]
    if match:
        return match[0]
    else:
        return None


def find_migu(title, artist):
    param = f"{artist}+{title}"
    for _ in range(2):
        rsp = requests.get(
            f"http://localhost:3400/song/find?keyword={param}", timeout=3).json()
        if "data" in rsp and "url" in rsp["data"] and rsp["data"]["url"]:
            found = {
                'title': escape(rsp["data"]["name"]),
                'artists': escape(';'.join([i["name"] for i in rsp["data"]["artists"]])),
                'url': rsp["data"]["url"],
                'source': 'migu'
            }
            if (title == found['title'] and artist == found['artists']) or \
                    title in found['title'] or found['title'] in title:
                return found
        print("\n    =!! not found, retrying... ")
        param = f"{title}"

    return None


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.exit(0)

    find(sys.argv[1], sys.argv[2])
