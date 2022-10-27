import helpers
import matches
from riotwatcher import LolWatcher
from league_apis import LCUApi, ReplayApi
import replay

import json
import os

class Config:
    def __init__(self, c):
        self.summoner_name = c["name"]
        self.summoner_region = c["region"]
        self.api_key = c["api_key"]
        self.nb_matches = c["nb_matches"]
    
    def print(self):
        print("---")
        print(f"¤ Configuration:")
        print(f" `- Chief Toplane Officer: {self.summoner_name}")
        print(f" `- Region: {self.summoner_region}")
        print(f" `- Number of matches to search for Yorick games: {self.nb_matches}")
        print("---")
        return

def main():
    os.system('cls')
    helpers.print_banner()
    with open("config.json", "r", encoding='utf-8') as f:
        conf = Config(json.load(f))
    conf.print()
    # TODO: validate the configuration
    helpers.ask_clean_files()
    input("¤ Please make sure that your League of Legends client is running and not busy. Press <Enter> to continue.")

    lolwatcher = LolWatcher(conf.api_key)
    puuid = helpers.get_summoner_puuid(lolwatcher, conf.summoner_name, conf.summoner_region)
    lcuapi = LCUApi()

    print("¤ New matches collection:")
    matches.get_new_data(lolwatcher, puuid, conf.summoner_region, conf.nb_matches)

    print("¤ Extracting replay data ...")
    matches.extract_replay_data(puuid)

    print("¤ Downloading replay files ...")
    matchidlist = [ gameid.removesuffix('.json') for gameid in os.listdir("replay_data")]
    for matchid in matchidlist:
        matches.download_replay(lcuapi,matchid)
    print(" `- Downloads started.")

    print(" `- Waiting for the first replay to be ready ...")
    filename = os.path.join(lcuapi.replay_path, f"{conf.summoner_region.upper()}-{matchidlist[0]}.rofl")
    helpers.wait_file(filename, 60)
    print(" `- Ready !")

    print("¤ Grab some popcorn, here we go.")
    print(f" `- Loaded games: {len(matchidlist)}")
    rapi = ReplayApi()
    for matchid in matchidlist:
        with open(os.path.join("replay_data", f"{matchid}.json")) as f:
            data = json.load(f)
        print(f" `- Match {matchid}: {len(data['tower_kill_events'])} towers bonked.")
        replay.start_replay(lcuapi, rapi, matchid, conf.summoner_name)
        
        [ replay.play_highlight(rapi, event["timestamp"]) for event in data["tower_kill_events"] ]

        replay.end(lcuapi, rapi)

    return



if __name__ == "__main__":
    main()
