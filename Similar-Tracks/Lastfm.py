import json, csv, time
import urllib, urllib2
from urllib2 import Request

#Obtain the json file of 100 similar tracks for Cher's Believe
params1 = urllib.urlencode({"method": "track.getSimilar", "track": "Believe", "artist": "Cher", "limit": "100",'api_key': '92cb33e97a63c5751f28e9102a38bb85', 'format':'json'})
url = "http://ws.audioscrobbler.com/2.0/";
request1 = urllib2.Request(url, params1)
response1 = urllib2.urlopen(request1)
r1 = response1.read()
d1 = json.loads(r1)

#List of  Mbid, Title, Artist for 100 similar tracks for Cher's Believe
tlist1 = [['MBID', 'TITLE', 'ARTIST']]

#Keeps track of 10 similar tracks for each of the 100 tracks obtained
tlist2 = [['SOURCE', 'TARGET']]

for i in d1['similartracks']['track']:
    title = i['name']
    art = i['artist']['name']
    mbid1 = i['mbid']

    if mbid1:
        tl1 = []
        tl1.append(mbid1);
        tl1.append(title)
        tl1.append(art.encode('utf-8'))
        tlist1.append(tl1);

        #Extract 10 similar tracks for each track
        try:
            params2 = urllib.urlencode({"method": "track.getSimilar", "track": title, "artist": art, "limit": "10",'api_key': '92cb33e97a63c5751f28e9102a38bb85', 'format':'json'})
            request2 = urllib2.Request(url, params2)
            response2 = urllib2.urlopen(request2)
            r2 = response2.read()
            d2 = json.loads(r2)
            time.sleep(0.1)
        except:
            pass

        for j in d2['similartracks']['track']:
            mbid2 = j['mbid']
            tl2 = []
            if mbid2:
                #Removes symmetric records
                for t in tlist2:
                    if t[0] == mbid2:
                        break
                else:        
                    tl2 = []
                    tl2.append(mbid1);
                    tl2.append(mbid2)
                    tlist2.append(tl2);        

#Write into CSV file
with open("tracks.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in tlist1:
        writer.writerow(line)
        
with open("track_id_sim_track_id.csv", "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in tlist2:
        writer.writerow(line)
            
  
