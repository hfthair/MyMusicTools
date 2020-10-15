import os
import json
import random
import time
import requests

with open('user_agents.txt', 'r') as f:
    agents = f.read().split('\n')

def random_ua():
    return random.choice(agents)

def download_migu(url, title, dst):
    ext = url.split('.')[-1]
    filename = f'{dst}/{title}.{ext}'
    if os.path.isfile(filename):
        print("  | already done")
        return

    r = requests.get(url, headers={'user-agent': random_ua()}, stream=True)
    if r.ok:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
        print("  | done")
    else:
        print("  ! Download error: ", r)

def download_ytm(url, title, dst):
    ext = 'm4a'
    filename = f"{dst}/{title}.{ext}"
    if os.path.isfile(filename):
        print("  | already done")
        return
    else:
        # todo: use as lib
        rename = filename.replace("'", "_")
        os.system(f"youtube-dl -f 'bestaudio[ext=m4a]' --embed-thumbnail --add-metadata --quiet -o '{rename}' '{url}'")
        print("  | done")

def download(playlist, dst):
    for k in playlist:
        song = playlist[k]

        title = song["title"]
        artist = song["artists"]
        url = song["url"]
        source = song["source"]

        print(f" # {title} ({artist}) <{source}>")
        if source == "ytm":
            download_ytm(url, title, dst)
        elif source == "migu":
            download_migu(url, title, dst)
        else:
            print("unkown source, ", source)

        time.sleep(random.random()*3)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.exit(0)

    download(sys.argv[1], sys.argv[2])
