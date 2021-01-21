from musicbrainzngs import get_artist_by_id, get_label_by_id, get_place_by_id, get_series_by_id, set_useragent
from musicbrainzngs.musicbrainz import ResponseError
from time import sleep
from json import dumps
from pandas import DataFrame, read_csv
from codecs import open

set_useragent('kp_lister', '0.0.1', contact='tom@kunsten.be')
with open("mbids_contemporary_music.txt", "r") as f:
    mbids = f.readlines()

records = []
for mbid in set(mbids):
    try:
        mb_data = get_artist_by_id(mbid.strip().split("/")[-1], includes=['url-rels'])["artist"]
    except ResponseError:
        try:
            mb_data = get_place_by_id(mbid.strip().split("/")[-1], includes=['url-rels'])["place"]
        except ResponseError:
            try:
                mb_data = get_label_by_id(mbid.strip().split("/")[-1], includes=['url-rels'])["label"]
            except ResponseError:
                mb_data = get_series_by_id(mbid.strip().split("/")[-1], includes=['url-rels'])["series"]
    print(mb_data)
    data = {
        "name": mb_data["name"],
        "mbid": mbid,
        "sort-name": mb_data["sort-name"] if "sort-name" in mb_data else None,
        "disambiguation": mb_data["disambiguation"] if "disambiguation" in mb_data else None,
        "country": mb_data["country"] if "country" in mb_data else None
    }
    if "url-relation-list" in mb_data:
        data["webpage"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "official" in url_rel["type"]])
        data["facebook"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "facebook.com" in url_rel["target"]])
        data["discogs"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "discogs.com" in url_rel["target"]])
        data["itunes"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "itunes.com" in url_rel["target"]])
        data["soundcloud"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "soundcloud.com" in url_rel["target"]])
        data["spotify"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "spotify.com" in url_rel["target"]])
        data["idagio"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "idagio.com" in url_rel["target"]])
        data["deezer"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "deezer.com" in url_rel["target"]])
        data["bandcamp"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "bandcamp.com" in url_rel["target"]])
        data["youtube"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "youtube.com" in url_rel["target"]])
        data["wikipedia"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "wikipedia.org" in url_rel["target"]])
        data["wikidata"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "wikidata.org" in url_rel["target"]])
        data["bandsintown"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "bandsintown.com" in url_rel["target"]])
        data["songkick"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "songkick.com" in url_rel["target"]])
        data["setlist"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "setlist.fm" in url_rel["target"]])
        data["matrix"] = ",".join([url_rel["target"] for url_rel in mb_data["url-relation-list"] if "matrix-new-music.be" in url_rel["target"]])
    records.append(data)

df = DataFrame.from_records(records)
df.to_excel("contemporary_music.xlsx", columns=["mbid", "name", "sort-name", "disambiguation", "country", "webpage", "matrix", "facebook", "discogs", "itunes", "soundcloud", "spotify", "idagio", "deezer", "bandcamp", "youtube", "bandsintown", "songkick", "setlist", "wikipedia", "wikidata"])
