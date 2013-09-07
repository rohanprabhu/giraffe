#!/usr/bin/python

from flask import Flask, request
from handler import GiraffeHandler

from girafferequest import GiraffeRequest

from decimal import *

import logging
import re

app = Flask(__name__)

logging.basicConfig(level="DEBUG")
giraffe = GiraffeHandler()

service_key = "8dde4af5-495b-4ef3-a934-bdb502cd9c24"

@app.route('/<mobile_hash>/')
def update_expense(mobile_hash):
    message = request.args.get('m')
    logging.debug("Got message `%s` for hash `%s`" % (mobile_hash, message))

    result = False
    send_back = None

    try:
        gr = GiraffeRequest(mobile_hash, message)

        # Awesome. Another hack!!! Fucking get rid of this.
        if gr.title.lower() == "account":
            try:
                accounts = giraffe.get_accounts(user=mobile_hash)
                message = ""
                total_amount = 0.0

                for account in accounts:
                    if account["direction"] == "owe":
                        total_amount -= float(''.join(re.findall("[0-9\.]+", account["amount"])))
                        message += "%s: pay %s<br />" % (account["friend"], account["amount"])
                    else:
                        total_amount += float(''.join(re.findall("[0-9\.]+", account["amount"])))
                        message += "%s: collect %s<br />" % (account["friend"], account["amount"])

                send_back = ("net: %s<br /><br />" % total_amount) + message
            except Exception as e:
                logging.debug("Could not fetch accounts %s" % e)
                send_back = "Could not get accounts"
        else:
            # TODO: Figure out how to remove this hack ASAP
            gr.users.append("You")

            bills = [((Decimal(gr.amount)/len(gr.users)).quantize(Decimal(10) ** -2), x) for x in gr.users]

            result = giraffe.add_expense(
                user=mobile_hash,
                title=gr.title,
                bills=bills)

            send_back = "Succesfully added expense %s (%s)" % (gr.title, str(Decimal(gr.amount)))
    except Exception as e:
        logging.debug("Request failed %s" % e)
        result = False
        send_back = "Could not add expense. Something's wrong :("

    response = '<html><head><meta name="txtweb-appkey" content="%s" /></head><body>%s</body></html>'

    return response % (service_key, send_back)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=37189)
