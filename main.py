#!/usr/bin/python3
import json
import flask
from flask import Flask
from random import sample
import hearthstone.hearth_api as hc
from sys import stdout

app = Flask(__name__)
# Define logger


def set_search_param(class_name):
    """
    Setup dictionary to search for Legendary cards with 7 or
    more mana of the specified class type
    """
    class_params = {
        "locale": "en_US",
        "set": "",
        "class": class_name,
        "manaCost": "7,8,9,10",
        "attack": "",
        "health": "",
        "collectible": "",
        "rarity": "legendary",
        "type": "",
        "minionType": "",
        "keyword": "",
        "gameMode": "",
    }
    # print(json.dumps(class_params, indent=4))
    return class_params


def query_cards():
    """Query for all Druid and Warlock legendary cards with 7 or greater mana cost."""
    hearth_query = hc.Hearth()
    battle_token = hearth_query.get_hearth_connection()
    combined_cards = []
    meta_query = {'set_id': {}, 'type_id': {}, 'rarity_id': {}, 'class_id': {}}
    warlock_data = hearth_query.query("cards", set_search_param('warlock'), battle_token)
    druid_data = hearth_query.query("cards", set_search_param('druid'), battle_token)
    app.logger.info("Warlock and Druid card data pulled")
    """
    Pull additional metadata to populate a dictionary of human readable data for the 
    set, type, class, and rarity fields. For sets there's a sub field of aliases 
    for the legacy card sets.
    """
    hearth_metadata = hearth_query.query("metadata", {"locale": "en_US"}, battle_token)
    for card_sets in hearth_metadata['sets']:
        meta_query['set_id'][card_sets['id']] = card_sets['name']
        if 'aliasSetIds' in card_sets:
            for alias in card_sets['aliasSetIds']:
                meta_query['set_id'][alias] = card_sets['name']
    for card_types in hearth_metadata['types']:
        meta_query['type_id'][card_types['id']] = card_types['name']
    for card_rarities in hearth_metadata['rarities']:
        meta_query['rarity_id'][card_rarities['id']] = card_rarities['name']
    for card_classes in hearth_metadata['classes']:
        meta_query['class_id'][card_classes['id']] = card_classes['name']
    app.logger.info("Metadata dictionary prepared")
    # print(json.dumps(meta_query, indent=4))
    """add the human readable fields to the card data"""
    for card in warlock_data['cards']:
        card['set_name'] = meta_query['set_id'][card['cardSetId']]
        card['type_name'] = meta_query['type_id'][card['cardTypeId']]
        card['rarity_name'] = meta_query['rarity_id'][card['rarityId']]
        card['class_name'] = meta_query['class_id'][card['classId']]
        combined_cards.append(card)
    for card in druid_data['cards']:
        card['set_name'] = meta_query['set_id'][card['cardSetId']]
        card['type_name'] = meta_query['type_id'][card['cardTypeId']]
        card['rarity_name'] = meta_query['rarity_id'][card['rarityId']]
        card['class_name'] = meta_query['class_id'][card['classId']]
        combined_cards.append(card)
    # print(json.dumps(combined_cards, indent=4))
    app.logger.info("Enriched card dictionary created.")
    return combined_cards


@app.route('/')
def hearthstone_query():
    """ display a random selection of 10 cards sorted by their ID"""
    sorted_cards = sorted(sample(query_cards(), 10), key=lambda obj: obj['id'])
    # print(json.dumps(sorted_cards, indent=4))
    app.logger.info("Random 10 cards selected and sorted by card id")
    return flask.render_template('index.html', cards=sorted_cards)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
