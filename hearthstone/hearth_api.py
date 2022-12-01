#!/usr/bin/python3

import os
import requests
import logging
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import json


class Hearth(object):
    def __init__(self):
        self.token_url = "https://us.battle.net/oauth/token"
        self.api_url = "https://us.api.blizzard.com/hearthstone"
        self.a_token = None
        self.header = None

    def get_hearth_connection(self):
        """
        Retrieve credentials from ENV and open a session
        with battle.net returns an access token
        """
        try:
            battle_secret = os.environ.get('BATTLE_SECRET')
            battle_id = os.environ.get('BATTLE_ID')
        except Exception:
            logging.error('ID or Secret is missing from env variables')
            return None
        client = BackendApplicationClient(client_id=battle_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url=self.token_url, client_id=battle_id, client_secret=battle_secret)
        access_token = dict(token)
        logging.info('Returning connection data')
        return access_token['access_token']

    def query(self, endpoint, query, battle_token):
        """
        Queries Hearthstone API endpoints based on parameters passed to it.
        """
        card_url = self.api_url + "/" + endpoint
        try:
            card_header = {"Authorization": "Bearer {token}".format(token=battle_token)}
            response = requests.get(card_url, headers=card_header, params=query)
            json_data = response.json()
            return json_data
        except Exception:
            if battle_token is None:
                logging.error("Token is missing. Auth failed.")
            else:
                logging.error("Query failed")
