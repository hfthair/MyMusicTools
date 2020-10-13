import os
import json
import random
import time
import requests

with open('user_agents.txt', 'r') as f:
    agents = f.read().split('\n')

def random_ua():
    return random.choice(agents)

def download(playlist, dst):
    with open(playlist, 'r', encoding='utf8') as f:
        playlist = json.load(f)

    for k in playlist:
        data = playlist[k]

        name = data["name"]
        artist = ';'.join([i["name"] for i in data["artists"]])
        url = data["url"]

        ext = url.split('.')[-1]

        filename = f'{dst}/{name}.{ext}'

        print("## ", name, "    ", end="")
        if os.path.isfile(filename):
            print("[already done]")
            continue

        r = requests.get(url, headers={'user-agent': random_ua()}, stream=True)
        if r.ok:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
            print("[done]")
        else:
            print("Download error: ", r)

        time.sleep(random.random()*3)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.exit(0)

    download(sys.argv[1], sys.argv[2])
