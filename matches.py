import os
from tqdm import tqdm
import json





# Discriminates relevant games. Checks if the game is 5v5 and the summoner is playing Yorick.
def yorick_filter(match_stat, puuid):
    if match_stat['info']['gameMode'] == "CLASSIC":
        idx = match_stat['metadata']['participants'].index(puuid)
        if match_stat['info']['participants'][idx]['championName'] == 'Yorick':
            return True
    return False
    
# Fetches the last N matches name from user match history by querying Riot API,
# Filters for new data by comparing these matches to existing files,
# Filters for Yorick games,
# Downloads the filtered match data, stores it to files and returns the stats list and the timelines list under \stats and \timelines.
def get_new_data(lolwatcher, puuid, region, nb_matches):    
    matchlist = lolwatcher.match.matchlist_by_puuid(region, puuid, count=nb_matches) # Gets a list with containing names of the last N matches
    existing_matches = [ filename.removesuffix('_timeline.json') for filename in os.listdir('timelines') ]
    new_matchlist = [ match for match in matchlist if match not in existing_matches ]
    new_counter = 0
    if len(new_matchlist) > 0:
        print(" `- Collecting data ...")
        for match in tqdm(new_matchlist):
            stat = lolwatcher.match.by_id(region, match)    # First get match stats so we can chek if this match is relevant

            if yorick_filter(stat, puuid) is True:
                timeline = lolwatcher.match.timeline_by_match(region, match)
                with open(os.path.join("timelines",f"{match}_timeline.json"), "w") as f:
                    json.dump(timeline,f)
                new_counter += 1

    print(f" `- {new_counter} relevant new matches found !")        
    return


# Extract useful events to replay from the matches timeline.
# Stores the extracted data under \replay_data.
def extract_replay_data(puuid):
    timelines = []
    for filename in os.listdir("timelines"):
        with open(f"timelines\\{filename}", "r") as f:
            timelines.append(json.load(f))

    existing_replay_data = os.listdir("replay_data")
    for timeline in timelines:
        gameid = timeline["info"]["gameId"]
        if f"{gameid}.json" not in existing_replay_data:
            data = {
                "game_id": gameid,
                "part_id": [ participant["participantId"] for participant in timeline["info"]["participants"] if participant["puuid"] == puuid ][0],
                "tower_kill_events": []
            }
            # Iterate through all events of the timeline and append every relevant event to data["tower_kill_events"] :
            # destroyed tower by the summoner identified by his participantId extracted earlier
            [ [ data["tower_kill_events"].append(event) for event in frame["events"] if event["type"] == "BUILDING_KILL" and event["killerId"] == data["part_id"] and event["buildingType"] == "TOWER_BUILDING" ] for frame in timeline["info"]["frames"] ]
            
            if len(data["tower_kill_events"]) > 0:     # Filter out games without tower kill, they are useless for the replays
                with open(f"replay_data\\{data['game_id']}.json", "w") as f:
                    json.dump(data ,f)
    print(" `- Done !")
    return 


# Downloads the replay file (.rofl file) for the given gameid)
def download_replay(api, gameid):
    res = api.get_replay_metadata(gameid)
    
    if res.status_code == 404 and 'create' in json.loads(res.content)["message"]:
        res = api.post_replay_metadata_create(gameid)
        if res.status_code == 204: download_replay(api, gameid)
        else: print(f'Something went wrong with POST /create', res.status_code, res.content)

    elif res.status_code == 200 :
        state = json.loads(res.content)["state"]
        if state == "download":
            res = api.post_replay_download(gameid)
            download_replay(api, gameid)

    else: print(f'Error with {gameid} :', res.status_code, res.content)
    return
