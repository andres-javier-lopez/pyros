#coding: utf-8

import pycurl
import StringIO
import random
import string
import time
import hashlib, hmac

url = "http://localhost:8080/"
auth_key = "1234"

class Test(object):
    def __init__(self):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)
    
    def run(self):
        self.restobject_test()
        self.auth_test()
        
    def restobject_test(self):
        rand = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
        req = ['', rand, rand + '/valores']
        for r in req:
            self._set_request(url + 'basic/' + r)
            methods = ['GET', 'POST', 'PUT', 'DELETE']
            for method in methods:
                self.c.setopt(pycurl.CUSTOMREQUEST, method)
                self._print_results()
    
    def auth_test(self):
        timestamp = str(int(time.time()))
        datastring = "GET /auth/?timestamp=" + timestamp
        hash = hmac.new(auth_key, datastring, hashlib.sha256).hexdigest()
        self._set_request(url + 'auth/?timestamp=' + timestamp + '&signature=' + hash)
        self.c.setopt(pycurl.CUSTOMREQUEST, 'GET')
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
