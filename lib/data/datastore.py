from pymongo import MongoClient

import logging

class DataStore:
    connection = None
    db = None
    db_conf = {
        "name": "giraffe",
        "host": "localhost",
        "port": 27017
    }

    @classmethod
    def connect(self):
        self.connection = MongoClient(host=self.db_conf["host"], port=self.db_conf["port"])
        self.db = self.connection[self.db_conf["name"]]

    @classmethod
    def set_credentials(self, user, username, password):
        logging.debug("Setting credentials for %s" % user)
        users = self.db["users"]
        users.update({"user": user}, {"$set": {"username": username, "password": password}}, True)
        logging.debug("Set credentials for %s" % username)

    @classmethod
    def get_credentials(self, user):
        logging.debug("Getting credentials for %s" % user)
        users = self.db["users"]
        user = users.find_one({"user": user}, {"username": True, "password": True})

        if(user is not None):
            return user["username"], user["password"]

    @classmethod
    def delete_all(self):
        self.db["users"].drop()

    @classmethod
    def get_friends_list(self, user):
        logging.debug("Getting friends for user %s" % user)
        users = self.db["users"]
        friend_list = users.find_one({"user": user}, {"friends": True})

        if(friend_list is None):
            return []
        else:
            print 

        ret = []

        for friend in friend_list["friends"]:
            ret.append(friend)

        return ret

    @classmethod
    def add_friend(self, user, friend):
        logging.debug("Adding friend for user")
        users = self.db["users"]

        users.update({"user": user}, {"$addToSet": {"friends": friend}}, True, False)
        logging.debug("Added friend [%s] for user [%s]" % (friend, user))

    @classmethod
    def disconnect(self):
        self.connection.disconnect()