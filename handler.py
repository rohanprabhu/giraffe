from lib.data.datastore import DataStore
from lib.dividely.dividelymanager import DividelyManager
from lib.dividely.credentials import Credentials

from datetime import datetime

import logging
import sys
import os

def last_exc_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print exc_type, fname, exc_tb.tb_lineno

class GiraffeHandler:
    ds = None
    dividely = None

    @classmethod
    def __init__(self):
        self.ds = DataStore()
        self.dividely = DividelyManager()
        self.ds.connect()

    @classmethod
    def add_expense(self, user, title, bills):
        try:
            username, password = self.ds.get_credentials(user)

            if(username == None or password == None):
                return False

            credentials = Credentials(username, password)
            short_codes = [x[1] for x in bills]
            friends_list = self.ds.get_friends_list(user, short_codes)
            emails = {x["short_code"]: x["email"] for x in friends_list}
            emails["You"] = "You"

            bill_objects = []

            for bill in bills:
                bill_objects.append((bill[0], emails[bill[1]]))

            self.dividely.add_expense(credentials, title, bill_objects, datetime.today().strftime("%m/%d/%Y"))
        except Exception as e:
            logging.debug("Failed request [%s]" % e)
            try:
            	last_exc_info()
                logging.debug("Last ditch attempt to logout")
                self.dividely.logout()
            except Exception as e:
            	logging.debug("Last ditch logout attempt fail. Need to figure this out immediately [%s]" % e)
                pass

            return False

        return True

    @classmethod
    def get_accounts(self, user):
        username, password = self.ds.get_credentials(user)
        friends = self.ds.get_friends_list(user, None)
        name_map = {x["email"]: x["name"] for x in friends}

        accounts = self.dividely.get_accounts(Credentials(username, password))
        accounts_final = []

        for account in accounts:
        	account["friend"] = name_map[account["friend"]]
        	accounts_final.append(account)

        return accounts_final

    @classmethod
    def __del__(self):
        try:
            self.ds.disconnect()
        except:
            pass

