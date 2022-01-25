import requests
import pymongo


def extract(url):
    data = requests.get(url)
    return data


def transform(data):
    client = pymongo.MongoClient()
    db = client['starwars']
    data = data.json()
    starships = data['results']
    for starship in starships:
        pilot_urls = starship['pilots']
        pilots = []
        for pilot in pilot_urls:
            info = requests.get(pilot)
            pilot_info = info.json()
            pilot_name = pilot_info['name']
            pilot_id = (db.characters.find_one({"name": pilot_name}, {"_id": 1}))['_id']
            pilots.append(pilot_id)
        starship['pilots'] = pilots
    return starships


def load(starships):
    client = pymongo.MongoClient()
    db = client['starwars']
    db.starships.insert_many(starships)


def starship_pilots(url):
    client = pymongo.MongoClient()
    db = client['starwars']
    db.starships.drop()
    db.create_collection("starships")

    while url is not None:
        data = extract(url)
        transformed_data = transform(data)
        load(transformed_data)
        url = data.json()['next']


starship_pilots("https://swapi.dev/api/starships")