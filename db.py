import pymongo

client = pymongo.MongoClient()
db = client["telegramLeaks"]
collection = db["telega"]


def create_many(data):
    collection.insert_many(data)

def create(data_dict):
    return collection.insert_one(data_dict).inserted_id


def read(elem_dict, combo_mult, limit):
    if limit==0:
        return collection.find(elem_dict).skip(combo_mult * 100)
    return collection.find(elem_dict).skip(combo_mult * 100).limit(limit)


def update(id, update_data):
    collection.update_one(id, {'$set': update_data})


def delete(id):
    collection.delete_one(id)
