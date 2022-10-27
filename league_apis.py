import base64
from signal import signal
import psutil
import re
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import os
import signal


# Class that interacts with the League Client API
class LCUApi:
    def __init__(self):
        (port, auth_token) = self.lol_process_info()
        self.port = port
        self.token = base64.b64encode(f"riot:{auth_token}".encode("utf-8")).decode("utf-8")
        self.base_url = f'https://127.0.0.1:{self.port}'
        self.replay_path = self.get_replay_path()

    # Returns the port and the remoting auth token that are necessary to request the LCU API
    # Based on the info present in the commandline of process 'LeagueClientUx.exe'
    def lol_process_info(self):
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'LeagueClientUx.exe':
                lol_process = proc
                break
        try:
            for i in lol_process.cmdline():
                r = re.search('^--remoting-auth-token=([^$]*)', i)
                if r:
                    auth_token = r.group(1)
                    break
            for i in lol_process.cmdline():
                r = re.search('^--app-port=([^$]*)', i)
                if r:
                    port = r.group(1)
                    break
            return (port, auth_token)
        except UnboundLocalError:
            print("ERROR : League Client process not found.")
            exit()
            

    def get_replay_path(self):
        url = f'{self.base_url}/lol-replays/v1/rofls/path'
        headers = {"accept": "application/json", "Authorization": f"Basic {self.token}"}
        response = requests.get(url=url, headers=headers, verify=False)
        path = os.path.abspath(response.content.decode('utf-8').strip('"'))
        return path

    # Gets the availability of the replay for a given gameid
    # 200 & "state":"download" => OK, we can download
    # 200 & "state":"incompatible" => KO, no way to get this replay
    # 200 & "state":"watch" => Replay is already downloaded
    # 200 & "state": "checking" => We don't know yet, have to retry
    # 404 & "message" contains "create endpoint first" => We must post /create first and get /metadata again
    def get_replay_metadata(self, gameid):
        url = f'{self.base_url}/lol-replays/v1/metadata/{gameid}'
        headers = {"accept": "application/json", "Authorization": f"Basic {self.token}"}
        response = requests.get(url=url, headers=headers, verify=False)
        return response


    # Creates the metadata of a given gameid so we can GET /metadata afterwards
    # WARNING: if we re-query too soon /metadata we can get "checking" status, so we don't know yet and should try again until we have the status
    def post_replay_metadata_create(self, gameid):
        url = f'{self.base_url}/lol-replays/v2/metadata/{gameid}/create'
        headers = {"accept": "*/*", "Authorization": f"Basic {self.token}", "Content-Type": "application/json"}
        body = json.dumps({"gameId": int(gameid)})
        response = requests.post(url=url,headers=headers,data=body,verify=False)
        return response
    
    # Download the .rofl file for the given gameid
    def post_replay_download(self, gameid):
        url = f'{self.base_url}/lol-replays/v1/rofls/{gameid}/download/graceful'
        headers = {"accept": "*/*", "Authorization": f"Basic {self.token}", "Content-Type": "application/json"}
        body = json.dumps({"gameId": int(gameid)})
        response = requests.post(url=url, headers=headers, data=body, verify=False)
        return response

    # Launch the replay for the given gameid
    def post_replay_watch(self, gameid):
        url = f'{self.base_url}/lol-replays/v1/rofls/{gameid}/watch'
        headers = {"accept": "*/*", "Authorization": f"Basic {self.token}", "Content-Type": "application/json"}
        body = json.dumps({"gameId": int(gameid)})
        response = requests.post(url=url, headers=headers, data=body, verify=False)
        return response

    # Get the UX state. Only following states will be useful in the code: '"ShowMain"', '"MinimizeAll"'
    def get_ux_state(self):
        url = f'{self.base_url}/riotclient/ux-state'
        headers = {"accept": "*/*", "Authorization": f"Basic {self.token}", "Content-Type": "application/json"}
        response = requests.get(url=url, headers=headers, verify=False)
        return response
    
    def post_ux_show(self):
        url = f'{self.base_url}/riotclient/ux-show'
        headers = {"accept": "*/*", "Authorization": f"Basic {self.token}", "Content-Type": "application/json"}
        body = ''
        response = requests.post(url=url, headers=headers, data=body, verify=False)
        return response


    # State may be '"ShowMain"' or '"MinimizeAll"'
    def wait_ux_state(self, state):
        res = self.get_ux_state()
        curr_state = res.content.decode('utf-8')
        if state == '"ShowMain"' and curr_state == '""':        # curr_state = '""' isntead of "ShowMain" when League Client was just launched so we take care of this
            self.post_ux_show()
        while curr_state != state:  
            time.sleep(0.5)    
            curr_state = self.get_ux_state().content.decode('utf-8')
        return 


# Class that interacts with the "replay" API to control the replay settings
# Make sure to enable this API in LoL config files for it to work
class ReplayApi():
    def __init__(self):
        self.base_url = "https://127.0.0.1:2999"
        self.session = requests.Session()
        self.session.verify = "riotgames.pem"
        self.playback_endpoint = self.base_url+"/replay/playback"
        self.recording_endpoint = self.base_url+"/replay/recording"
        self.render_endpoint = self.base_url+"/replay/render"
        self.game_endpoint = self.base_url+"/replay/game"
        return

    def post(self, endpoint_url, data):
        response = self.session.post(endpoint_url, data=json.dumps(data).encode())
        return response

    def get(self, endpoint_url):
        response = self.session.get(endpoint_url)
        return response

    # Exits the replay
    def exit(self):
        pid = self.game_get_process_id()
        os.kill(pid, signal.SIGINT)
        

    # Waits that the riot API is ready (=the replay has started)
    def wait_for_ready(self):
        while True:
            try:
                self.session.headers = {'Content-Type': 'application/json'}
                res = self.session.get(self.render_endpoint)
                if res.status_code == 200:
                    break
                else:
                    time.sleep(2)
            except requests.exceptions.ConnectionError:         # May be raised if we test too soon
                time.sleep(2)
                continue
        return
    
    def game_get_process_id(self):
        response = self.get(self.game_endpoint)
        id = json.loads(response.content.decode("utf-8"))["processID"]
        return id

    # Pauses the playback
    def playback_pause(self):
        settings = {'paused': True}
        response = self.post(self.playback_endpoint, settings)
        return response
    
    # Starts the playback
    def playback_start(self):
        settings = {'paused': False}
        response = self.post(self.playback_endpoint, settings)
        return response

    # Go to the timestamp provided in SECONDS
    def playback_set_timestamp(self, timestamp):
        settings = {'time': timestamp}
        response = self.post(self.playback_endpoint, settings)
        return response

    # Disables a few things on the screen for a better experience
    def render_prepare(self):
        settings = {'interfaceAll': False, 'healthBarMinions': False, 'healthBarPets': False, 'healthBarChampions': False, 'floatingText': False}
        response = self.post(self.render_endpoint, settings)
        return response

    def camera_attach_to(self, name):
        settings = {"cameraMode": "fps", "cameraAttached": True, "selectionName": name, "selectionOffset": { "x": 1200.0 , "y": 1000.0, "z": -1200.0}, "cameraRotation": {"x": -45.0, "y": 30.0, "z": 0.0}}
        response = self.post(self.render_endpoint, settings)
        return response

