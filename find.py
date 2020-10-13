import os
import json
import requests

def escape(x):
    return x.replace('&', '').replace('?', '').replace('=', '').replace('#', '')

def find(src, dst):
    with open(src, 'r', encoding='utf8') as f:
        songs = json.load(f)

    out = {}
    if os.path.isfile(dst):
        with open(dst, 'r', encoding='utf8') as f:
            out = json.load(f)

    for s in songs:
        name = escape(s['name'])
        artist = ''
        if s['artists']:
            artist = s['artists'][0]['name']
        artist = escape(artist)
        key = f"{name}-{artist}"

        if key in out and "url" in out[key] and out[key]["url"]:
            print('## ', key, "[already done] ==>",
                out[key]["name"], '-', ";".join([i["name"] for i in out[key]["artists"]]))
            continue

        param = f"{artist}+{name}"
        for _ in range(2):
            print('## ', key, end="")
            r = requests.get(f"http://localhost:3400/song/find?keyword={param}")
            rsp = r.json()
            if "data" in rsp and "url" in rsp["data"] and rsp["data"]["url"]:
                out[key] = rsp["data"]
                new_name = rsp["data"]["name"]
                new_artist = ''
                if rsp["data"]["artists"]:
                    new_artist = rsp["data"]["artists"][0]["name"]
                if not new_artist:
                    new_artist = artist
                print(' ==>', new_name, '-', new_artist)
                break
            else:
                print("==!! Failed: ", key)
                # print(rsp)
                param = f"{name}"

    with open(dst, 'w', encoding='utf8') as f:
        json.dump(out, f)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.exit(0)

    find(sys.argv[1], sys.argv[2])
