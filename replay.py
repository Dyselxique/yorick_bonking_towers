import time
from math import floor



# Launch the replay for the given matchid and fixes the camera on the given summoner.
def start_replay(lcuapi, rapi, matchid, name):
    lcuapi.wait_ux_state('"ShowMain"')
    lcuapi.post_replay_watch(matchid)
    rapi.wait_for_ready()
    rapi.camera_attach_to(name)
    rapi.render_prepare()
    return


# Sets the player to the given timestamp and plays the replay for 7 seconds
def play_highlight(rapi, timestamp):
    tstamp = floor(timestamp/1000)
    rapi.playback_set_timestamp(tstamp-7)
    time.sleep(10)
    return


# Quits the replay
def end(lcuapi, rapi):
    rapi.exit()
    lcuapi.wait_ux_state('"ShowMain"')




