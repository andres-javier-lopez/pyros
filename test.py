#coding: utf-8

import pycurl
import StringIO
import random
import string
import time
import hashlib, hmac
import json

url = "http://localhost:8080/"
auth_key = "1234"

class Test(object):
    def __init__(self):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
    
    def run(self):
        self.restobject_test()
        self.auth_test()
        self.database_test()
        
    def restobject_test(self):
        rand = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
        req = ['', rand, rand + '/valores']
        for r in req:
            for method in self.methods:
                self._make_request('basic/' + r, method)
    
    def auth_test(self):
        for method in self.methods:
            timestamp = str(int(time.time()))
            datastring = method + " /auth/?timestamp=" + timestamp
            hash = hmac.new(auth_key, datastring, hashlib.sha256).hexdigest()
            self._make_request('auth/?timestamp=' + timestamp + '&signature=' + hash, method)
    
    def database_test(self):
        data = json.dumps({"valor1": "test", "valor2": "5" })
        self._make_request('test1', 'POST', body=data)
    
    def _make_request(self, url_string, method, body = None):
        self._set_request(url + url_string)
        self.c.setopt(pycurl.CUSTOMREQUEST, method)
        if(body is not None):
            self.c.setopt(pycurl.POSTFIELDS, body)
        else:
            self.c.setopt(pycurl.POSTFIELDS, "")
        self._print_results()
        
    def _set_request(self, request):
        self.c.setopt(pycurl.URL, request)
    
    def _print_results(self):
        b = StringIO.StringIO()
        self.c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.c.perform()
        print b.getvalue()
        b.close()

if __name__ == '__main__':
    test = Test()
    test.run()
