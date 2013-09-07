#!/usr/bin/python

from flask import Flask, request
from handler import GiraffeHandler

from girafferequest import GiraffeRequest

from decimal import *

import logging

app = Flask(__name__)

logging.basicConfig(level="DEBUG")
giraffe = GiraffeHandler()

service_key = "8dde4af5-495b-4ef3-a934-bdb502cd9c24"

@app.route('/<mobile_hash>/')
def update_expense(mobile_hash):
    message = request.args.get('m')
    logging.debug("Got message `%s` for hash `%s`" % (mobile_hash, message))

    result = False

    try:
        gr = GiraffeRequest(mobile_hash, message)

        # TODO: Figure out how to remove this hack ASAP
        gr.users.append("You")

        bills = [((Decimal(gr.amount)/len(gr.users)).quantize(Decimal(10) ** -2), x) for x in gr.users]

        result = giraffe.add_expense(
            user=mobile_hash,
            title=gr.title,
            bills=bills)
    except:
        result = False

    send_back = None

    if(result is True):
        send_back = "Succesfully added expense %s (%s)" % (gr.title, str(Decimal(gr.amount)))
    else:
        send_back = "Could not add expense. Something's wrong :("

    response = '<html><head><meta name="txtweb-appkey" content="%s" /></head><body>%s</body></html>'

    return response % (service_key, send_back)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=37189)
