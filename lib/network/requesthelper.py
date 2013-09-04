import httplib, urllib, urllib2, cookielib
import logging

from urlparse import urlparse

class RequestHelper:
    @staticmethod
    def postCall(url, headers, data):
        return RequestHelper.httpCall("POST", url, headers, data)

    @staticmethod
    def getConnection(scheme, host):
    	conn = None
    	if(scheme == 'http'):
    		logging.debug('Non-SSL scheme requested')
    		conn = httplib.HTTPConnection(host)
    	else:
    		logging.debug('SSL scheme requested')
    		conn = httplib.HTTPSConnection(host)

    	return conn

    @staticmethod
    def httpCall(method, url, headers, data):
        urlParts = urlparse(url)
        logging.debug("Preparing connection to %s", urlParts.netloc)
        conn = RequestHelper.getConnection(urlParts.scheme, urlParts.netloc)
 
        logging.debug("Calling url %s with data `%s` and headers `%s`", url, data, headers)
        conn.request(method, urlParts.path, data, headers)
 
        response = conn.getresponse()
        data = response.read()
        logging.debug("Got response with status %s", response.status)
        conn.close()

        print response.getheaders()
 
        return data, response.status
