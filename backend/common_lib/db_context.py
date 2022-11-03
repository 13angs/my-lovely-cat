import pymongo, os


class DbContext:
    db = None
    collection = None
    mongo_url = ''

    def __init__(self, mongo_url, db_name:str, coll_name: str) -> None:
        client = pymongo.MongoClient(mongo_url)
        self.db = client[db_name]
        self.collection = self.db[coll_name]

    def first(self, query):
        return self.collection.find_one(query)
    
    def find(self, query: dict=None, selection: dict=None):
        return self.collection.find(query, selection)
        # if query != None:
        #     for doc in self.collection.find(query, selection):
        #         return doc

        # for doc in self.collection.find():
        #     return doc

    def callback(self, docs: list):
        self.collection.insert_one(docs)
    
    def save(self, message: dict) -> bool:
        try:
            self.callback(message)
            return True
        except:
            return False


class MessageDbContext(DbContext):
    def __init__(self, mongo_url) -> None:
        DbContext.__init__(self,mongo_url,  'my_lovely_cat_db', 'messages')
        self.mongo_url = mongo_url

    def callback(self, message: dict):
        super().callback(message)

        user_ctx = UserDbContext(self.mongo_url)
        user_ctx.save(message)

class UserDbContext(DbContext):
    def __init__(self, mongo_url) -> None:
        DbContext.__init__(self, mongo_url, 'my_lovely_cat_db', 'users')

    def callback(self, message: dict):
        events = message['events']
        dest = message['destination']

        for event in events:
            msg_type = event['type']
            if msg_type == 'follow':
                # TODO:
                # - [ ] find the user
                # - [ ] if not exist insert it
                user_id = event['source']['userId']
                query = {"user_id": user_id}
                user = self.first(query)
                if user is None:
                    user_doc = {"user_id": user_id, "dest": dest}
                    self.collection.insert_one(user_doc)
