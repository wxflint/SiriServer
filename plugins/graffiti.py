# Author: SNXRaven (Jonthon Nickols)
#!/usr/bin/python


import urllib2
import json

from plugin import *

class test(Plugin):
    req = urllib2.Request("http://siri.grwh.net/api/")
    full_json = urllib2.urlopen(req).read()
    load = json.loads(full_json)
    Command = load['value']['inputCommand']
    Command = Command.replace('&quot;','\"')
    print("Commands loadded from Manager: \n" + Command + " \n")
    @register("en-US", Command)
    def st_hello(self, speech, language):
        if language == 'en-US':
            req = urllib2.Request("http://siri.grwh.net/api/")
	    full_json = urllib2.urlopen(req).read()
	    load = json.loads(full_json)
	    store = load['value']['response']
	    store = store.replace('&quot;','\"') 
	    self.say(store)
        self.complete_request()