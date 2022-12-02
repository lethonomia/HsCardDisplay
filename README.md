# Hearthstone card display                                                                                                                                       
         
Queries the Hearthstone API on BattleNet and pulls down all Hearthstone cards that meet the requirements below.
- Class: Druid or Warlock
- Mana: 7 or greater
- Rarity: Legendary

The Flask app will serve a webpage that displays a table of 10 cards randomly selected from both sets that were retrieved from 
the Hearthstone DB. The fields in the table are listed below.
- Name
- Class
- Type
- Rarity
- Set
- Card image (with card id on hover)

## Installation
Pull the repo and install the required python libraries.
```
git clone https://github.com/lethonomia/HsCardDisplay.git
pip3 install -r requirements.txt
```
Set up your client and secret with battleNet 
```
https://develop.battle.net/documentation/guides/getting-started
```

## Configuration
### Secrets
The app expects the client id and client secret to be available as environmental variables. 

**Locally** 
```
export BATTLE_ID="client-id"
export BATTLE_SECRET="client-secret"
```
**Docker**
```
-e BATTLE_ID="client-id" -e BATTLE_SECRET="client-secret"
```
For production, this would be replaced with an industry standard secret solution (Vault, Parameter Store, etc.).

### Flask Port
**Locally**
The port is set in the main.py to 8080.
```
app.run(host='0.0.0.0', port=8080, debug=False)
```

**Docker**
The port is exposed in the docker file and set in the run command.
```
-p 8080:8080
```

## Running

### Locally
After exporting the client id and secret the app can be started by calling main.py
```
python3 main.py
```

### Docker
The docker container uses a base python image that is publicly accessible.
After building the container it can be run using the container name. 
```
docker build ./ -t hearthstone
docker run --rm -it -p 8080:8080 -e BATTLE_ID="client-id" -e BATTLE_SECRET="client-secret" hearthstone:latest
```

## TODO
- remove duplicate code for adding human-readable info to the cards with module 
- extend logging to auth and query classes
- expand querying to additional classes and mana costs

## Resources Used
- [Hearthstone GameData API](https://develop.battle.net/documentation/hearthstone/game-data-apis)
- [BattleNet API Guide](https://develop.battle.net/documentation/guides)