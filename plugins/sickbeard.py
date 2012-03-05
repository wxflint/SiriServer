#!/usr/bin/python

# sickbeard.py
# Created by Nurfballs

#Version 0.2

IPAddress = "IPADDRESS"
Port = "PORT"
APIKey = "APIKEY"

import re, urlparse
import urllib2, urllib
import json
from urllib2 import urlopen
from xml.dom import minidom

from plugin import *

from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class define(Plugin):
 
    # ------------------------------------------
    # - Display upcoming shows -
    # -------------------------------------------
    @register("en-US", ".*new.*(tv|episode|show).*")
    def sb_newshows(self, speech, language):
        SickBeardURL = u'http://%s:%s/api/%s/?cmd=future&sort=date&type=today|missed|soon' % (IPAddress,  Port,  APIKey)
        try:
            # Query SickBeard for new / missed shows
            jsonResponse = urllib2.urlopen(SickBeardURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            self.say("Here is a list of new shows this week:")
            view = AddViews(self.refId, dialogPhase="Completion")
            
            AnswerString = ''
            # Get missed shows -
            for show in jsonDecoded['data']['missed']:
                AnswerString = AnswerString + show['airs'] + ': ' + show['show_name'] + '\n'
            SickBeardAnswerMissed = AnswerObject(title='Missed Shows:',lines=[AnswerObjectLine(text=AnswerString)]) 
            
            # Get shows airing today
            AnswerString = ''
            for show in jsonDecoded['data']['today']:
                AnswerString = AnswerString + show['airs'] + ': ' + show['show_name'] + '\n'   
            SickBeardAnswerToday = AnswerObject(title='Airing Today:',lines=[AnswerObjectLine(text=AnswerString)])
            
            # Get shows airing soon
            for show in jsonDecoded['data']['soon']:
                AnswerString = AnswerString + show['airs'] + ': ' + show['show_name'] + '\n'   
            SickBeardAnswerUpcoming = AnswerObject(title='Upcoming Shows:',lines=[AnswerObjectLine(text=AnswerString)])
            
            view1 = 0
            view1 = AnswerSnippet(answers=[SickBeardAnswerMissed, SickBeardAnswerUpcoming])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            self.complete_request()
        except (urllib2.URLError):
            self.say("Sorry, a connection to SickBeard could not be established.")
            self.complete_request()

    # -----------------------------
    # - Add new show
    # -----------------------------
    
    #@register("en-US",  "(download tv show [a-zA-Z0-9]+)")
    @register("en-US", "(download) .*(tv) (show|shows)* ([\w ]+)")
    def sb_download(self,  speech,  language,  regex):
        ShowTitle = regex.group(regex.lastindex)
        Query = urllib.quote_plus(ShowTitle.encode("utf-8"))
        SickBeardURL = 'http://%s:%s/api/%s/?cmd=sb.searchtvdb&name=%s' % (IPAddress,  Port,  APIKey,  str(Query))
               
        jsonResponse = urllib2.urlopen(SickBeardURL).read()
        jsonDecoded = json.JSONDecoder().decode(jsonResponse)

        # Get number of matches found
        ShowCount = len(jsonDecoded['data']['results'])
        
        
        #No matches found
        if ShowCount == 0:
            self.say("Sorry, I couldnt find any matches for that show.")
            self.complete_request()
                                    
        # Exact match found
        elif ShowCount == 1:
            TVDBID = jsonDecoded['data']['results'][0]['tvdbid']
            ShowName = jsonDecoded['data']['results'][0]['name']
            AddShowURL = 'http://%s:%s/api/%s/?cmd=show.addnew&tvdbid=%s' % (IPAddress,  Port,  APIKey,  TVDBID)
    
            #Add the show to SickBeard
            jsonResponse = urllib2.urlopen(AddShowURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
    
            #If successful:
            if jsonDecoded['result'] == "success":
                self.say(str(ShowName) + " successfully added to SickBeard.")
                self.complete_request()
                    
            #If failed:
            else:
                self.say("Oops! " + jsonDecoded['message'])
                self.complete_request()
                    
        elif ShowCount > 1 and ShowCount < 5 :
            self.say("I found " + str(ShowCount) + " matches for that show.")
            AnswerString = ''
            Count = 0
            for j in xrange(0, ShowCount):
                Count = Count + 1
                AnswerString = AnswerString + str(Count) + ": " + str(jsonDecoded['data']['results'][j]['name']) + '\n'
            
            SickBeardAnswer = AnswerObject(title='Top ' + str(ShowCount) + ' Matches:',lines=[AnswerObjectLine(text=AnswerString)])
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = 0
            view1 = AnswerSnippet(answers=[SickBeardAnswer])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            
            self.say("I dont know how to handle multiple matches just yet. Check back when I have been updated.")
            self.complete_request()  
        # More than five matches found
        else:
            self.say("I found " + str(ShowCount) + " matches for that show.")
            self.say ("Here are the first 5.")
                        
            AnswerString = ''
            for j in xrange(1,  6):
                AnswerString = AnswerString + str(j) + ": " + str(jsonDecoded['data']['results'][j]['name']) + '\n'
                            
            SickBeardAnswer = AnswerObject(title='Top 5 Matches:',lines=[AnswerObjectLine(text=AnswerString)])
            view = AddViews(self.refId, dialogPhase="Completion")
            view1 = 0
            view1 = AnswerSnippet(answers=[SickBeardAnswer])
            view.views = [view1]
            self.sendRequestWithoutAnswer(view)
            
            self.say("I dont know how to handle multiple matches just yet. Check back when I have been updated.")
            self.complete_request()  

    # --------------------------------
    # - Restart Sickbeard -
    # --------------------------------
    @register("en-US", "sickbeard.*(restart|reboot|reset).*")       
    def sb_restart(self,  speech,  language):  
        SickBeardURL = u'http://' + str(IPAddress) + ':' + str(Port) + '/api/' + str(APIKey) +  '/?cmd=sb.restart'
        try:
            jsonResponse = urllib2.urlopen(SickBeardURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            if jsonDecoded['result'] == "success":
                self.say("Command sent successfully. Sickbeard is now restarting.")
            else:
                self.say("Something went wrong. The command returned a failure. Please try again")
        
        except (urllib2.URLError):
            self.say("Sorry, a connection to SickBeard could not be established.")
            self.complete_request()
            
        
