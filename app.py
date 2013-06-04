#!/usr/bin/env python

# Flask
import os
import urllib2
from flask import request
from flask import Flask
from flask import Response

# json to csv
from StringIO import StringIO
from json import load
from urllib import urlopen
from urllib import urlencode
from pandas import DataFrame

app = Flask(__name__)

@app.route('/')
def json2csv():
    sql = request.args.get('q')
    if sql == None:
        status = 400
        response = 'You must send a ?q= parameter.'
    else:
        url = 'https://box.scraperwiki.com/cc7znvq/47d80ae900e04f2/sql/'
        query_string = urlencode({'q':sql})
        handle = urlopen(url + '?' + query_string)
        if handle.code == 200:
            s = StringIO()
            df = DataFrame(load(handle))
            df.to_csv(s)
            status = 200
            response = s.getvalue()
        else:
            status = handle.code
            response = handle.read()

    return Response(response=response, status=status, content_type='application/json')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
