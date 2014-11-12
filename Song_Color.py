import json, urllib2, subprocess, random, time

class Song_Color:

    def __init__(self, sid, name, artist):
        time.sleep(3.2)
        print "Getting " + name + " by " + artist
        url = "http://developer.echonest.com/api/v4/track/" \
              "profile?api_key=AFUD2LVWLLXSYMNBC&" \
              "format=json&bucket=audio_summary&id="
        url += "spotify:track:" + sid

        try :
            response = urllib2.urlopen(url).read()
        except urllib2.HTTPError, err:
            if err.code == 429 :
                print "Too many requests... waiting 80 seconds",
                time.sleep(80)
                print "...Done waiting!"
                response = urllib2.urlopen(url).read()

        data = json.loads(response.decode('utf-8'))
        # print data['response']['track']['audio_summary']
        try :
            value = data['response']['track']['audio_summary']
            # print value[:-10]
            self.aValue = value
            self.speech = value['speechiness']
            self.tempo = value['tempo']
            self.energy = value['energy']
            self.liveness = value['liveness']
            self.acoustic = value['acousticness']
            self.dance = value['danceability']
            self.valence = value['valence']
            self.loudness = value['loudness']
        except :
            self.aValue = "{}"
            self.speech     = 0
            self.tempo      = 0
            self.energy     = 0
            self.liveness   = 0
            self.acoustic   = 0
            self.dance      = 0
            self.valence    = 0
            self.loudness   = 0
        # self.speech = random.random()
        # self.dance = random.random()
        # self.energy = random.random()
        self.id = sid
        self.name = name
        self.artist = artist

        if self.dance  == None : self.dance  = 0
        if self.speech == None : self.speech = 0
        if self.energy == None : self.energy = 0


def rgb_to_hex(rgb_value):
    return '#%02x%02x%02x' % rgb_value

def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip('#')
    return tuple(int(hex_value[i:i + len(hex_value) // 3], 16)for i in range(0, len(hex_value), len(hex_value)//3))

urlTarget = "https://api.spotify.com/v1/users/{{USER}}/playlists/{{PLAYLIST_ID}}/tracks"
urlHeader = "Authorization: Bearer BQAe0Ae8S_RXxi8x13qhfc2K0cGVx0pAp4rJMMBHB8bVCKh6VdQ-LFfcZeRxhzEMZdupxnHBvdswrC4PZXYc7udnTwp7rpBkCXsv0Vihz8-WSRPMaAKwEK478K12NLbIht8Z5FJxxDVWaRoHjE3eiuvcoQuAhtS6Obdp_oB3I0wAJA6FLYsV6lopIJnPsQRKxxUiJIF6J_DDt4iAYkI31gcdEcRhMezD6C8Nh-ZHDSJPxQNr74ryuFQErTnzfMc0eJmN"

def getTrackIDsFromPlaylist(playlistID, userID) :
    curlCommand = ['curl', '-X', "GET", urlTarget.replace("{{USER}}", userID)             \
                                                 .replace("{{PLAYLIST_ID}}", playlistID), \
                                                 '-H', urlHeader]

    subp = subprocess.Popen(curlCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    curlstdout, curlstderr = subp.communicate()
    response = str(curlstdout)
    # print str(curlstdout) + " " + str(curlstderr)

    trackList = json.loads(response)
    # print response
    toRet = []
    items = trackList["items"]
    for i in items :
        toRet.append([i["track"]["id"], i["track"]["name"], i["track"]["artists"][0]["name"]])
    return toRet


count = 0

def dealWithTrackIDList(trackList) :
    global count
    toRet = []
    for t in trackList :
        count = count + 1
        toRet.append(Song_Color(t[0], t[1], t[2]))
    return toRet

#"",
SongColorList = []
playlistIDs = [                                                                            \
    "12121113853||6Ba7ixQdl3uTDqC1X8uxbr"  , "spotify||6LBZwjKY0VZLoe79qeGcCF",           \
    "spotify||5FJXhjdILmRA2z5bvz4nzf"      , "spotify||4hOKQuZbraPDIfaGbM3lKI",           \
    "spotify||3ZgmfR6lsnCwdffZUan8EA"      , "spotify||3qu74M0PqlkSV76f98aqTd",           \
    "ljfullofgrace||2WzN4LYiBENoB7bKD3YbFq", 
    "spotify||63dDpdoVHvx5RkK87g4LKk" ,           \
    "spotify||0QvUYQKpZmrah6QRrcUEWK"      , "12121113853||77glGmUcFaU1mhYudqkPup"        \
    "spotify||7xADHS7Ryc6oMdqBVhNVQ9"
]

def getSCAsText(sc) :
    return str(sc.aValue)
    # try : 

    #     # toRet = {}
    #     # toRet["name"] = sc.name
    #     # toRet = "name:"+sc.name+"||artist:"+sc.artist+"||speech:"+str(sc.speech)+"||tempo:"+str(sc.tempo)+"||energy:"+str(sc.energy)+"||liveness:"+str(sc.liveness)+"||acoustic:"+str(sc.acoustic)+"||dance:"+str(sc.dance)+"||valence:"+str(sc.valence)+"||loudness:"+str(sc.loudness)+"\n"

    # except :
    #     return ""
    # return toRet

f = open("results.txt", "a")

for s in playlistIDs :
    temp = s.split("||")
    p = temp[1]
    u = temp[0]
    track = getTrackIDsFromPlaylist(p, u)
    idList = dealWithTrackIDList(track)
    toWrite = ""
    for i in idList :
        scAsText = getSCAsText(i)
        if scAsText != "" :
            f.write(scAsText.encode("ascii", "ignore"))
            print scAsText

print "Scraped " + str(count) + " songs"
