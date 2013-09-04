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
    def get_friends_list(self, user):
        logging.debug("Getting friends for user %s" % user)
        friends = self.db["friends"]
        friend_list = friends.find({"user": user})

        ret = []

        for friend in friend_list:
            ret.append(friend)

        return ret

    @classmethod
    def add_friend(self, user, friend):
        logging.debug("Adding friend for user")
        friends = self.db["friends"]

        friends.update({"user": user}, {"$addToSet": {"friends": friend}}, True, False)
        logging.debug("Added friend [%s] for user [%s]" % (friend, user))

    @classmethod
    def disconnect(self):
    	self.connection.disconnect()
