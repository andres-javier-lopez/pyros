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
                print self._make_request('basic/' + r, method)['mensaje']
    
    def auth_test(self):
        for method in self.methods:
            timestamp = str(int(time.time()))
            datastring = method + " /auth/?timestamp=" + timestamp
            hash = hmac.new(auth_key, datastring, hashlib.sha256).hexdigest()
            print self._make_request('auth/?timestamp=' + timestamp + '&signature=' + hash, method)['mensaje']
    
    def database_test(self):
        data = json.dumps({"valor1": u"test_á", "valor2": "5" })
        result = self._make_request('test1', 'POST', body=data)
        assert(result['success'])
        print "insertado elemento"
        
        result = self._make_request('test1', 'GET')
        id_result = result['elementos'][-1]['id_test']
        print "el id es " + str(id_result)
        
        result = self._make_request('test1/' + str(id_result), 'GET')
        assert(result['elemento']['valor1'] == u"test_á")
        assert(result['elemento']['valor2'] == "5")
        print "comparado elemento"
        
        result = self._make_request('test1/?search=test_á', 'GET')
        id_compare = result['elementos'][-1]['id_test']
        assert(id_compare == id_result)
        result = self._make_request('test1/?value=5', 'GET')
        id_compare = result['elementos'][-1]['id_test']
        assert(id_compare == id_result)
        result = self._make_request('test1/?search=test_á&value=5', 'GET')
        id_compare = result['elementos'][-1]['id_test']
        assert(id_compare == id_result)
        print "buscando elemento"
        
        data = json.dumps({"valor1": "test2", "valor2": 7})
        result = self._make_request('test1/' + str(id_result), 'PUT', body=data)
        assert(result['success'])
        print "reemplazados valores"
        
        result = self._make_request('test1/' + str(id_result), 'GET')
        assert(result['elemento']['valor1'] == "test2")
        assert(result['elemento']['valor2'] == "7")
        print "verificado reemplazo"
        
        data = json.dumps({"prueba": "42"})
        result = self._make_request('test1/' + str(id_result), 'POST', body=data)
        assert(result['success'])
        print "insertado subelemento"
        
        result = self._make_request('test1/' + str(id_result), 'GET')
        id_sub = result['elemento']['subtest'][-1]['id_test2']
        print "el id del subelemento es " + id_sub
        
        result = self._make_request('test2/' + str(id_sub), 'GET')
        assert(result['elemento']['prueba'] == "42")
        print "verificado subelemento"
        
        result = self._make_request('test2/' + str(id_sub), 'DELETE')
        assert(result['success'])
        print "eliminado subelemento"
        
        result = self._make_request('test1/' + str(id_result), 'DELETE')
        assert(result['success'])
        print "elemento eliminado"
    
    def _make_request(self, url_string, method, body = None):
        self._set_request(url + url_string)
        self.c.setopt(pycurl.CUSTOMREQUEST, method)
        if(body is not None):
            self.c.setopt(pycurl.POSTFIELDS, body)
        else:
            self.c.setopt(pycurl.POSTFIELDS, "")
        
        result = self._get_results()
        try:
            return json.loads(result)
        except ValueError:
            print method + ' ' + url_string + ' ' + str(body)
            raise Exception('Finalizar ejecución')
        
    def _set_request(self, request):
        self.c.setopt(pycurl.URL, request)
    
    def _get_results(self):
        b = StringIO.StringIO()
        self.c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.c.perform()
        value = b.getvalue()
        b.close()
        return value

if __name__ == '__main__':
    test = Test()
    test.run()
