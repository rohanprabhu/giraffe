import urllib, urllib2, cookielib
import logging
import time
import re

from bs4 import BeautifulSoup

class DividelyManager:
    access_token = None
    opener = None
    logged_in = False
    cj = None

    urls = {
        "mainpage": "https://dividely.com",
        "login": "https://dividely.com/session",
        "split": "https://dividely.com/split",
        "bills": "https://dividely.com/bills",
        "logout": "https://dividely.com/logout",
        "friends": "https://dividely.com/friends"
    }

    @classmethod
    def innerHTML(self, element):
        return "".join([str(x) for x in element.contents])

    @classmethod
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    @classmethod
    def get_authenticity_token(self, url, form_action):
        logging.debug("Getting authenticity token from dividely [action=%s, url=%s]" % (form_action, url))
        resp = self.opener.open(url)
        soup = BeautifulSoup(resp.read())

        formtag  = soup.find('form', attrs={'action': form_action})
        at_input = formtag.find('input', attrs={'name': 'authenticity_token'})
        authenticity = at_input.attrs["value"]
        logging.debug("Got authenticity token %s" % authenticity)
        return authenticity

    @classmethod
    def login(self, credentials):
        logging.debug("Attemtping to login for user %s" % credentials.username)

        authenticity = self.get_authenticity_token(form_action = '/session',
            url = self.urls["mainpage"])

        login_data = urllib.urlencode({"email": credentials.username,
            "password": credentials.password,
            "authenticity_token": authenticity})

        login_resp = self.opener.open(self.urls["login"], login_data)        
        logging.debug("Probably logged in %s" % login_resp)

    @classmethod
    def get_user_numbers(self):
        logging.debug("Attempting to get user number [current login context]")
        resp = self.opener.open(self.urls["split"])

        soup = BeautifulSoup(resp.read())
        opboxes = soup.findAll('select')

        usernumbers = {}

        for opbox in opboxes:
            all_ops = opbox.findAll('option')

            for op in all_ops:
                usernumbers[self.innerHTML(op)] = op.attrs["value"]

        logging.debug("Got usernumbers %s" % usernumbers)
        return usernumbers

    @classmethod
    def logout(self):
        logging.debug("Logging out")
        self.opener.open(self.urls["logout"])
        logging.debug("Logout request made")

    @classmethod
    def get_accounts(self, credentials):
        logging.debug("Getting accounts")
        pattern = "[+-]?[0-9]{1,3}(?:,?[0-9]{3})*(?:\.[0-9]{2})"
        self.login(credentials)
        resp = self.opener.open(self.urls["friends"])

        soup = BeautifulSoup(resp.read())
        data_cells = soup.findAll('td', attrs = {'class': 'ce'})

        logging.debug("Got accounts with %d friends" % (len(data_cells)/3))
        accounts = [None] * (len(data_cells)/3)
        index = 0

        for data_cell in data_cells:
            if index%3 == 0:
                accounts[index/3] = {}

                try:
                    accounts[index/3]["friend"] = self.innerHTML(data_cell.find('a')).strip()
                except:
                    accounts[index/3]["friend"] = ""
            elif index%3 == 1:
                try:
                    message = self.innerHTML(data_cell)
                    accounts[index/3]["direction"] = "owe"

                    if(message.find("You owe") != -1):
                        accounts[index/3]["direction"] = "collect"

                    accounts[index/3]["amount"] = re.findall(pattern, message)[0].strip()
                except:
                    accounts[index/3]["amount"] = ""
                    accounts[index/3]["direction"] = ""


            index = index + 1

        self.logout()
        return accounts

    @classmethod
    def add_expense(self, credentials, title, bills, date):
        self.login(credentials)
        logging.debug("Adding expense")
        total_amount = 0
        usernumbers = self.get_user_numbers()
        authenticity = self.get_authenticity_token(form_action = '/bills',
            url = self.urls["split"])

        add_bills = []

        req = []
        req.append(("paying_user", usernumbers["You"]))
        req.append(("description", title))
        req.append(("date", date))
        req.append(("kind", "shared"))
        req.append(("recur", "false"))
        req.append(("paypal", "false"))
        req.append(("commit", "Save"))
        req.append(("dir", "to"))
        req.append(("send_email", "false"))
        req.append(("authenticity_token", authenticity))

        for bill in bills:
            total_amount += bill[1]

            if(bill[0] not in usernumbers):
                raise ValueError("User not added %s" % bill[0])

            add_bills.append((usernumbers[bill[0]], bill[1]))

        for add_bill in add_bills:
            req.append(("friend[]", add_bill[0]))
            req.append(("friend_%s_amt" % add_bill[0], add_bill[1]))
            req.append(("friend_%s_spl" % add_bill[0], "even"))

        req.append(("amount", total_amount))

        req_data = urllib.urlencode(req)

        resp = self.opener.open(self.urls["bills"], req_data)
        logging.debug("Made request to add expense. Most probably must have succeeded")
        self.logout()
