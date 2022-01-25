import pymongo
from pprint import pprint as pp

client = pymongo.MongoClient()
db = client['starwars']
# print(db) # To check the db currently in

# print(db.list_collection_names())  # List all the collections in the db
# print(db.command({'listCollections': 1, 'filter': {'name': 'characters'}}))    # To show validators for the characters collection

# db.characters.insert_one({'name': 'Guri Demuria',
#                           'height': 195,
#                           'mass': 95})   # Inerts a dict in the db, use many instead of one for more entries

# db.characters.update_one({'name': 'Guri Demuria'}, {'$set': {'height': 194}})  # update/add info to Guri
# db.characters.update_one({'name': 'Guri Demuria'}, {'$set': {'hair_color': 'brown'}})

# db.characters.delete_one({'name': 'Guri Demuria'})  # Delete the entry Guri Demuria

# find_all = db.characters.find({})   # Show all the dictionaries stored in the collection
# pp(find_all[0])     # Show the first entry

# find_filter = db.characters.find({'$and': [{'height': {'$lte': 180}}, {'hair_color': {'$in': ['black', 'brown']}}]},
#                                  {'_id': 0, 'name': 1, 'height': 1, 'hair_color': 1})       # Filter and display necessary info
# pp(list(find_filter))

# agg = db.characters.aggregate([
#     {'$match': {'$and': [{'hair_color': {'$in': ['black', 'brown']}}, {'eye_color': 'brown'}]}},
#     {'$group': {'_id': "Hair color either black or brown and eye color brown", 'count': {'$sum': 1}}}
#     ])      # Aggregating the columns
# pp(list(agg))

# agg = db.characters.find({'$and': [{'hair_color': {'$in': ['black', 'brown']}}, {'eye_color': 'brown'}]},
#                          {'name': 1, 'hair_color': 1, 'eye_color': 1, '_id': 0})
# pp(list(agg))   # Check the above

# join = db.starships.aggregate([{'$lookup': {'from': 'characters', 'localField': 'pilots', 'foreignField': '_id', 'as': 'pilots'}}])
# pp(list(join))  # Join the two collections using _id as primary key for characters

# proj = db.characters.aggregate([{'$project': {'_id': 0,
#                                               'name': 1,
#                                               'homeworld.name': 1,
#                                               'species.name':
#                                                   {'$cond': {
#                                                       'if': {'$eq': ["", "$species.name"]},
#                                                       'then': '$$REMOVE',
#                                                       'else': '$species.name'
#                                                   }},
#                                               'height and mass': ['$height', '$mass']}}])
# pp(list(proj))  # To show required values

# character_ids = list(db.characters.find({}, {'_id': 1}))
# character_ids = [i['_id'] for i in character_ids]
# print(character_ids)