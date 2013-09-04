#!/usr/bin/python

from flask import Flask, request
from handler import GiraffeHandler

import logging

app = Flask(__name__)

logging.basicConfig(level="DEBUG")
giraffe = GiraffeHandler()

service_key = "8dde4af5-495b-4ef3-a934-bdb502cd9c24"

@app.route('/<mobile_hash>/')
def update_expense(mobile_hash):
    reponse = '''
    <html>
      <head>
       <meta name="txtweb-appkey" content="%s" />
      </head>
      <body>%s</body>
    </html>
    '''

    send_back = None

    try:
        giraffe.add_expense()
        send_back = "Expense added"
    except:
    	send_back = "Something went wrong!!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=37189)
