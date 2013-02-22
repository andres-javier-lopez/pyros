#coding: utf-8

import pycurl
import StringIO

request = "http://localhost:8080/try/"

class Test(object):
    def run(self):
        self.init_curl()
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        for method in methods:
            b = StringIO.StringIO()
            self.c.setopt(pycurl.WRITEFUNCTION, b.write)
            self.c.setopt(pycurl.CUSTOMREQUEST, method)
            self.c.perform()
            print b.getvalue()
            b.close()
        
    def init_curl(self):
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.URL, request)
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)


if __name__ == '__main__':
    test = Test()
    test.run()
