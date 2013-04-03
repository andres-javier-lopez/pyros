#coding: utf-8

import pycurl, StringIO, json, urllib2

class Request(object):
    def __init__(self, url, **kwargs):
        super(Request, self).__init__(**kwargs)
        self.url = url
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.FOLLOWLOCATION, 1)
        self.c.setopt(pycurl.MAXREDIRS, 5)
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
    
    def _make_request(self, url_string, method, body = None, headers = None):
        self._set_request(self.url + urllib2.quote(unicode(url_string).encode('utf-8'), '/?&='))
        self.c.setopt(pycurl.CUSTOMREQUEST, method)
        if(body is not None):
            self.c.setopt(pycurl.POSTFIELDS, body)
        else:
            self.c.setopt(pycurl.POSTFIELDS, "")
            
        if headers is not None:
            self.c.setopt(pycurl.HTTPHEADER, headers)
        
        result = self._get_results()
        try:
            return json.loads(result)
        except ValueError:
            print method + ' ' + url_string + ' ' + str(body)
            raise Exception(u'Finalizar ejecución')
        
    def _set_request(self, request):
        self.c.setopt(pycurl.URL, request)
    
    def _get_results(self):
        b = StringIO.StringIO()
        self.c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.c.perform()
        value = b.getvalue()
        b.close()
        return value

