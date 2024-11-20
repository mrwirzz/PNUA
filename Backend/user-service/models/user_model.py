from pymongo import MongoClient

class UserModel:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, data):
        return self.collection.insert_one(data)

    def get_users(self):
        return list(self.collection.find({}, {"_id": 0}))

    def update_preferences(self, user_id, preferences):
        return self.collection.update_one(
            {"_id": user_id},
            {"$set": {"preferences": preferences}}
        )

    def delete_user(self, user_id):
        return self.collection.delete_one({"_id": user_id})