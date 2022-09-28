from pymongo import MongoClient


class DBHandler:
    def __init__(self, db_name, collection_name):
        host = "host.docker.internal"
        port = "27017"
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(host, int(port))

    # insert
    def insert_item_one(self, data):
        result = self.client[self.db_name][self.collection_name].insert_one(data).inserted_id
        return result

    def insert_item_many(self, datas):
        result = self.client[self.db_name][self.collection_name].insert_many(datas).inserted_ids
        return result

    # find
    def find_item_one(self, condition=None):
        result = self.client[self.db_name][self.collection_name].find_one(condition, {"_id": False})
        return result

    def find_item(self, condition=None):
        result = self.client[self.db_name][self.collection_name].find(condition, {"_id": False})
        return result

    def find_text_search(self, text=None):
        result = self.client[self.db_name][self.collection_name].find({"$text": {"$search": text}})
        return result

    # update
    def update_item_one(self, condition=None, update_value=None):
        result = self.client[self.db_name][self.collection_name].update_one(filter=condition, update=update_value)
        return result

    def update_item_many(self, condition=None, update_value=None):
        result = self.client[self.db_name][self.collection_name].update_many(filter=condition, update=update_value)
        return result

    # delete
    def delete_item_one(self, condition=None):
        result = self.client[self.db_name][self.collection_name].delete_one(condition)
        return result

    def delete_item_many(self, condition=None):
        result = self.client[self.db_name][self.collection_name].delete_many(condition)
        return result

