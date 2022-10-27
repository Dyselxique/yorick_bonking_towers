# Yorick Bonking Towers
![](http://ddragon.leagueoflegends.com/cdn/img/champion/splash/Yorick_1.jpg)

Hey fellow Yorick mains, feel free to download and use this piece of code to watch your tower bonks.

## Disclaimers

- This code works for Windows version of League. It would need small modifications to work for Linux versions of League.
- It will encrypt all your files if an Irelia game is found so use at your own risks. I'm watching you.
- Maybe disclaimer n°2 is a joke, maybe not. Read the source code to make sure. Or just don't play the Ionian b*tch.
- You may use this program to watch other Yorick players, but I didn't test the case where the desired player to watch is on a different region than the region for which your League Client is configured (for example, you play in EUW1 and you would like to watch the tower bonks of a NA1 player).
- Disclaimer n°2 is a joke.

## Installation

- Get Python3 if you don't have it. Python 3.11 is available [here](https://www.python.org/downloads/windows/) and easy to install.
- Download / clone this repository.
- Make sure the Replay API is enabled in your game settings. The config file is located here (depending on how you installed the game) : `%LeagueInstallDirectory%\Config\game.cfg`. If the `EnableReplayApi` entry is not present, just add it under `[General]`. Restart your League Client.
```
[General]
EnableReplayApi=1
```
- Open a cmd and go inside the yorick_bonking_towers directory. [(help for beginners)](https://www.geeksforgeeks.org/cd-cmd-command/)
- Run the following command to make sure you have all the dependencies installed.
```
pip install -r requirements.txt 
```
- Edit config.json (more details below) to fit your need

## Configuration File (config.json)
To use this tool, you just need to provide 4 things in the config.json file before running.
```
{
    "name": "Yorick 0n Crack",
    "region": "euw1",
    "api_key": "RGAPI-aaaaaaaa-1111-cccc-2222-30c53f8adefa",
    "nb_matches": 10
}
```
- `name`: Your summoner name, strange utf-8 characters should be supported but I did not test it.
- `region`: Your region. Acceptable values are: `br1`, `eun1`, `euw1`, `jp1`, `kr`, `la1`, `la2`, `na1`, `oc1`, `tr1`.
- `api_key`: A Riot API key, to be able to query some of the Riot APIs. You can request one [here](https://developer.riotgames.com/), it is valid for 24 hours. If it expires you can just renew it. Wait a couple seconds after requesting a new API key so all Riot systems can get updated before you run yorick_bonking_towers.
- `nb_matches`: The amount of last games to search for Yorick games.

## Running the program

- Make sure you have a valid API key in `config.json`. Renew it through Riot Dev Portal if needed.
- Make sure your League of Legends client is running.
- Open a cmd and go inside yorick_bonking_towers directory.
- Run the following command to run the program
```
python main.py
```

That's it, enjoy ! :)

### Known issue during install

You may encounter an error during the installation of the dependencies. If you do not already have the python module `psutil`, an error will occur during the installation, saying that you need "C++ Build Tools". Just follow the microsoft link in the error, run the vs_installer executable and install C++ Build Tools with defaults. Then you can re-run the `pip` command to install the dependencies.
