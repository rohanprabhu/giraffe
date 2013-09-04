#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

@app.route('/<mobile_hash>/<message>')
def hello_world(mobile_hash, message):
    print mobile_hash, message
    return '<html><head><meta name="txtweb-appkey" content="8dde4af5-495b-4ef3-a934-bdb502cd9c24" /></head><body>RP/GK</body></html>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=37189)

