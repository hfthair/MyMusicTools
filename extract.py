import random
import requests

with open('user_agents.txt', 'r') as f:
    agents = f.read().split('\n')

def random_ua():
    return random.choice(agents)

def netease_playlist(play_id):
    url = f"https://api.mtnhao.com/playlist/detail?id={play_id}"
    rsp = requests.request("GET", url, headers={'user-agent': random_ua()}).json()
    sid = [i["id"] for i in rsp["playlist"]["trackIds"]]

    songs = []
    for i in range(0, len(sid), 200):
        strid = str(sid[i:i+200])
        url = f"http://music.163.com/api/song/detail?ids={strid}"
        rsp = requests.request("GET", url, headers={'user-agent': random_ua()}).json()

        for s in rsp["songs"]:
            title = s['name']
            artists = ";".join([i["name"] for i in s["artists"]])

            songs.append((title,artists))

    return songs


if __name__ == '__main__':
    import sys
    import json
    import pprint
    if len(sys.argv) != 2:
        sys.exit(0)

    r = netease_playlist(sys.argv[1])
