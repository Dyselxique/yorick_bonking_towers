import time
import os
from riotwatcher import ApiError

def print_banner():
    banner = """
                                                        
  ,--.   ,--.            ,--.      ,--.               
   \  `.'  /,---. ,--.--.`--' ,---.|  |,-.            
    '.    /| .-. ||  .--',--.| .--'|     /            
      |  | ' '-' '|  |   |  |\ `--.|  \  \            
      `--'  `---' `--'   `--' `---'`--'`--'           
  ,-----.                 ,--.    ,--.                
  |  |) /_  ,---. ,--,--, |  |,-. `--',--,--,  ,---.  
  |  .-.  \| .-. ||      \|     / ,--.|      \| .-. | 
  |  '--' /' '-' '|  ||  ||  \  \ |  ||  ||  |' '-' ' 
  `------'  `---' `--''--'`--'`--'`--'`--''--'.`-  /  
  ,--------.                                  `---'   
  '--.  .--',---. ,--.   ,--. ,---. ,--.--. ,---.     
     |  |  | .-. ||  |.'.|  || .-. :|  .--'(  .-'     
     |  |  ' '-' '|   .'.   |\   --.|  |   .-'  `)    
     `--'   `---' '--'   '--' `----'`--'   `----'     

Hey dude, I'm ghoul n°3. Have a seat, grab some popcorn, let's watch your last tower bonks.
-------------------------------------------------------------------------------------------"""
    print(banner)
    time.sleep(1)
    return


def print_exit_banner():
    banner = """
         ▄▀▀▄▀▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄   ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄   
        █   █   █ ▐  ▄▀   ▐ █  █ ▀  █ ▐  ▄▀   ▐ █  █ ▀  █ ▐ ▄▀   █ ▐  ▄▀   ▐ █   █   █   
        ▐  █▀▀█▀    █▄▄▄▄▄  ▐  █    █   █▄▄▄▄▄  ▐  █    █   █▄▄▄▀    █▄▄▄▄▄  ▐  █▀▀█▀    
         ▄▀    █    █    ▌    █    █    █    ▌    █    █    █   █    █    ▌   ▄▀    █    
        █     █    ▄▀▄▄▄▄   ▄▀   ▄▀    ▄▀▄▄▄▄   ▄▀   ▄▀    ▄▀▄▄▄▀   ▄▀▄▄▄▄   █     █     
        ▐     ▐    █    ▐   █    █     █    ▐   █    █    █    ▐    █    ▐   ▐     ▐     
                   ▐        ▐    ▐     ▐        ▐    ▐    ▐         ▐                    
     ▄▀▀▀█▀▀▄  ▄▀▀▀▀▄           ▄▀▀▄▀▀▀▄  ▄▀▀▄▀▀▀▄  ▄▀▀▀▀▄   ▄▀▀▀█▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▄▄▄▄  
    █    █  ▐ █      █         █   █   █ █   █   █ █      █ █    █  ▐ ▐  ▄▀   ▐ █ █    ▌ 
    ▐   █     █      █         ▐  █▀▀▀▀  ▐  █▀▀█▀  █      █ ▐   █       █▄▄▄▄▄  ▐ █      
       █      ▀▄    ▄▀            █       ▄▀    █  ▀▄    ▄▀    █        █    ▌    █      
     ▄▀         ▀▀▀▀            ▄▀       █     █     ▀▀▀▀    ▄▀        ▄▀▄▄▄▄    ▄▀▄▄▄▄▀ 
    █                          █         ▐     ▐            █          █    ▐   █     ▐  
    ▐                          ▐                            ▐          ▐        ▐        
                 ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀█▀▄    ▄▀▀█▄▄   ▄▀▀█▄▄▄▄  ▄▀▀▄ ▀▄                  
                █  █ ▀  █ ▐ ▄▀ ▀▄ █   █  █  █ ▄▀   █ ▐  ▄▀   ▐ █  █ █ █                  
                ▐  █    █   █▄▄▄█ ▐   █  ▐  ▐ █    █   █▄▄▄▄▄  ▐  █  ▀█                  
                  █    █   ▄▀   █     █       █    █   █    ▌    █   █                   
                ▄▀   ▄▀   █   ▄▀   ▄▀▀▀▀▀▄   ▄▀▄▄▄▄▀  ▄▀▄▄▄▄   ▄▀   █                    
                █    █    ▐   ▐   █       █ █     ▐   █    ▐   █    ▐                    
                ▐    ▐            ▐       ▐ ▐         ▐        ▐                         
"""
    print(banner)
    return


# Asks the user for deleting existing data. Useful if you mess with the files and stats/timelines are not symmetric.
def ask_clean_files():
    clean = input("¤ Do you want to clean all existing data ? Replays files (.rofl) will remain untouched. (y/N)")
    if clean in ["y"]:
        [ [ os.remove(os.path.join(dir_path,filename)) for filename in os.listdir(dir_path) ] for dir_path in ["timelines", "replay_data"] ]
        print(" `- Done !")
    elif clean in ["n", ""]:
        pass
    else:
        ask_clean_files()
    return


# Fetches summoner puuid (identifier) by querying Riot API and returns it
def get_summoner_puuid(lolwatcher, name, region):
    print("¤ Getting your puuid:")
    try:
        puuid = lolwatcher.summoner.by_name(region, name)["puuid"]
        print(f" `- {puuid}")
        return puuid
    except ApiError as e:
        if "403" in str(e):
            print("ERROR : Could not get your puuid. Received Error 403. Check your API key, renew it via https://developer.riotgames.com/ if it has more than 24 hours. Wait a couple seconds after renewing your key so Riot systems can update it.")
        else:
            print(e)
        exit()

#
def wait_file(abs_path, duration):
    timeout = duration
    print
    while(timeout > 0):
        if os.path.isfile(abs_path):
            return
        else:
            timeout -= 1
            time.sleep(1)
    print("ERROR : Could not find the file before timeout")
    exit()
    