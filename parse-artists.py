import json

artist_list = []

with open('output.json') as a:
    loaded = json.load(a)

for t in loaded["playlists"][0]["tracks"]:
    for a in t["track"]["artists"]:
        artist_list.append(a["name"])

unique_artist_list = list(set(artist_list))

for ua in unique_artist_list:
    # print("Artist: " + ua + "\n")
    f = open('./docs/artists/' + ua.replace('/', '_') + '.md', "a")
    f.write(
    "# " + ua + "\n\n"
    "|Track|Artist|\n"
    "|-----|----|\n"
    )
    for t in loaded["playlists"][0]["tracks"]:
        for a in t["track"]["artists"]:
            if a["name"] == ua:
                f.write("|" + t["track"]["name"] + "|" + ua + "|\n")
                # print(ua + " has " + t["track"]["name"])
    f.close()