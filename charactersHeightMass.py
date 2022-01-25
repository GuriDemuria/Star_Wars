import pymongo


client = pymongo.MongoClient()
db = client['starwars']

def extract():
    characters = []
    characters_db = db.characters.find({})
    for i in characters_db:
        characters.append(i)
    return characters

def transform(characters):
    for character in characters:
        if character['height'] == 'unknown':
            character['height'] = None
        else:
            character['height'] = int(character['height'])

    for character in characters:
        if character['mass'] == 'unknown':
            character['mass'] = None
        else:
            character['mass'] = character['mass'].replace(',','')
            character['mass'] = float(character['mass'])

    return characters

def load(characters):
    db.characters.drop()
    db.create_collection("characters")
    db.characters.insert_many(characters)


# load(transform(extract()))