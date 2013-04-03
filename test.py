#coding: utf-8

import random
import string
import time
import hashlib, hmac
import json
from base64 import b64encode
from pyrostest import tester

url = "http://localhost:8080/"
auth_key = "1234"

class Test(tester.Request):
    def __init__(self, url, **kwargs):
       super(Test, self).__init__(url, **kwargs)
    
    def run(self):
        self.restobject_test()
        self.auth_test()
        self.http_auth_test()
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
            data = json.dumps({"prueba": "áéíóúñ"})
            datastring = unicode(method + u" /auth/?data=áéíóúñ&timestamp=" + timestamp + ' ' + data)
            hash = hmac.new(auth_key, datastring.encode('utf-8'), hashlib.sha256).hexdigest()
            print self._make_request(u"auth/?data=áéíóúñ&timestamp=" + timestamp + '&signature=' + hash, method, body=data)['mensaje']
            
    def http_auth_test(self):
        userAndPass = b64encode(b"hola:mundo").decode("ascii")
        authString = str('Authorization: Basic ' + userAndPass)
        headers = [ authString ]
        for method in self.methods:
            print self._make_request(u"httpauth/", method, headers=headers)['mensaje']
            
    
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
        
        result = self._make_request(u'test1/?search=test_á', 'GET')
        id_compare = result['elementos'][-1]['id_test']
        assert(id_compare == id_result)
        result = self._make_request('test1/?value=5', 'GET')
        id_compare = result['elementos'][-1]['id_test']
        assert(id_compare == id_result)
        result = self._make_request(u'test1/?search=test_á&value=5', 'GET')
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

if __name__ == '__main__':
    test = Test(url)
    test.run()
