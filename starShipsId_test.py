from starShipsId import *
import pymongo

client = pymongo.MongoClient()
db = client['starwars']
url = "https://swapi.dev/api/starships"
data = extract(url)

def test_extract():
    e_data = extract(url).json()
    assert e_data['count'] == 36
    assert e_data['next'] == "https://swapi.dev/api/starships/?page=2"
    assert e_data['previous'] is None

def test_transform():
    t_data = transform(data)
    character_ids = list(db.characters.find({}, {'_id': 1}))
    character_ids = [i['_id'] for i in character_ids]
    for pilots in t_data:
        for pilot in pilots['pilots']:
            assert pilot in character_ids


def test_load():
    assert 'starships' in db.list_collection_names()
    assert db.starships.count_documents({}) == 36

def test_starship_pilots():
    starship_pilots(url)
    assert 'starships' in db.list_collection_names()
    assert db.starships.count_documents({}) == extract(url).json()['count']

    starship_elem = len(extract(url).json()['results'][0])
    for i in db.starships.find():
        assert len(i) == starship_elem + 1  # +1 to account for ObjectID in MongoDB

    query = db.starships.find({"name": "Millennium Falcon"}, {"pilots": 1, "_id": 0})[0]['pilots']
    character_ids = list(db.characters.find({}, {'_id': 1}))
    character_ids = [i['_id'] for i in character_ids]

    assert query[0] in character_ids
    assert query[1] in character_ids
    assert query[2] in character_ids
    assert query[3] in character_ids
