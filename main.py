import os
import json
import fire
import extract
import find
import download

def netease_dl(playlist, output):
    ### extract
    print(f"## extract playlist {playlist} ...", end="")

    pltmp = f'{output}/netease_{playlist}.json'
    if os.path.isfile(pltmp):
        with open(pltmp, 'r', encoding='utf8') as f:
            pl = json.load(f)
        print(f" | use cached ({len(pl)}) songs.")
    else:
        pl = extract.netease_playlist(playlist)
        print(f" | ({len(pl)}) songs")

    if not pl:
        print("## nothing extracted.")
    with open(pltmp, 'w', encoding='utf8') as f:
        json.dump(pl, f)

    ### find
    print(f"\n## search from other platforms ...")
    findtmp = f'{output}/found.json'
    found = {}
    if os.path.isfile(findtmp):
        with open(findtmp, 'r', encoding='utf8') as f:
            found = json.load(f)
        print(f" | load cached ({len(found)}) songs.")
    found = find.find(pl, found)
    if found:
        with open(findtmp, 'w', encoding='utf8') as f:
            json.dump(found, f)
    print(f" | found total ({len(found)}) songs.")

    ### download
    print(f"\n## downloading ...")
    music_dir = f'{output}/music'
    if not os.path.isdir(music_dir):
        os.mkdir(music_dir)
    download.download(found, music_dir)

if __name__ == '__main__':
    fire.Fire(netease_dl)

