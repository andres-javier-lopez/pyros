#coding: utf-8

import pycurl
import StringIO
import random
import string

request = "http://localhost:8080/basic/"

class Test(object):
    def __init__(self):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, request)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)
    
    def run(self):
        self.restobject_test()
        
    def restobject_test(self):
        rand = ''.join(random.choice(string.lowercase + string.digits) for i in range(4))
        req = ['', rand, rand + '/valores']
        for r in req:
            self.set_request(request + r)
            methods = ['GET', 'POST', 'PUT', 'DELETE']
            for method in methods:
                b = StringIO.StringIO()
                self.c.setopt(pycurl.WRITEFUNCTION, b.write)
                self.c.setopt(pycurl.CUSTOMREQUEST, method)
                self.c.perform()
                print b.getvalue()
                b.close()
        
    def set_request(self, request):
        self.c.setopt(pycurl.URL, request)

if __name__ == '__main__':
    test = Test()
    test.run()
