import pymongo
client = pymongo.MongoClient()
db = client.get_database('spider')
c = db.get_collection('test')
c.insert_one({'name':'wangwu','age':23,'identity':'student'})