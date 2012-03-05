#sabnzbd.py

#Sabnzbd+ Plugin
#by Casey (Nurfballs) Mullineaux 

#Version 0.1 - Initial release

#Usage: 
# -- View current queue --
# *(sab|sabnzbd|download).*(queue|q)*
# Example: say "download queue" 

#-- Pause Sabnzbd --
# (download|downloads).*(pause|stop)*
# Example: say "downloads pause"

# -- Resume Sabnzbd --
# (download|downloads).*(resume|unpause|start)*
# Example: say "downloads resume"

# -- 

# =================================
# INSERT YOUR INFO HERE
# =================================
IPAddress ="10.1.1.199"
Port = "8800"
APIKey = "81ff9235c94991993d0ae5f19c9342ef"
# =================================

import re, urlparse
import urllib2, urllib
import json
import math
from urllib2 import urlopen
from xml.dom import minidom

from plugin import *


from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine

class define(Plugin):
 
    # ------------------------------------------
    # - Display current download queue -
    # -------------------------------------------
    @register("en-US", "(sab|sabnzbd|download).*(queue|q)*")
    def sab_displayqueue(self, speech, language):
        SabnzbdURL = 'http://%s:%s/sabnzbd/api?mode=qstatus&output=json&apikey=%s' % (IPAddress,  Port,  APIKey)
        try:
            jsonResponse = urllib2.urlopen(SabnzbdURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            # If something is downloading - show ALL the things!
            if jsonDecoded['noofslots'] > 0:
            
                self.say("Here is your current Sabnzbd+ queue:")
                view = AddViews(self.refId, dialogPhase="Completion")
            
                # --- Statistics ---
                AnswerStringQueueStats = ''
            
                #Get the queue status
                if jsonDecoded['paused'] == True:
                    QueueStatus = 'Paused'
                else:
                    QueueStatus = 'Downloading'
                AnswerStringQueueStats = AnswerStringQueueStats + 'Status: ' + QueueStatus + '\n'
                    
                #Get number of items in the queue
                NumberOfItems = jsonDecoded['noofslots']  
                AnswerStringQueueStats = AnswerStringQueueStats + 'Queue Size: ' + str(NumberOfItems) + ' items\n'
            
                # Get current download speed
                DownloadSpeed = jsonDecoded['speed']
                AnswerStringQueueStats = AnswerStringQueueStats + 'Download Speed: ' + str(DownloadSpeed) + ' \n'
            
                # Get time left to complete all downloads
                TimeLeft = jsonDecoded['timeleft']
                AnswerStringQueueStats = AnswerStringQueueStats + 'Time Remaining: ' + str(TimeLeft) + ' \n'
            
                QueueMB = round(jsonDecoded['mb'])                                      # Get size of queue
                QueueMBLeft = round(jsonDecoded['mbleft'])                          # Get how much is left of queue
                QueueMBDone = round(QueueMB - QueueMBLeft)                      # Calculate how much has been downloaded
                QueueProgress = round(((QueueMBDone / QueueMB) * 100),2)  # Calculate percentage downloaded
                
                AnswerStringQueueStats = AnswerStringQueueStats + 'Progress: %s%% (%s MB / %s MB)' % (QueueProgress,  QueueMBDone,  QueueMB)
                
                # Output to the AnswerObject
                SabnzbdAnswerQueueStats = AnswerObject(title='Statistics:',lines=[AnswerObjectLine(text=AnswerStringQueueStats)]) 
                
                # --- Current Download ---
               
                # Get the name of the item currently downloading
                AnswerStringCurrentDownload = ''
                AnswerStringCurrentDownload = AnswerStringCurrentDownload + str(jsonDecoded['jobs'][0]['filename']) + '\n'
                
                # Get size statistics
                CurrentJobMB = round(jsonDecoded['jobs'][0]['mb'], 2)               # Get size of current job
                CurrentJobMBLeft = round(jsonDecoded['jobs'][0]['mbleft'], 2)  # Get how much is left of current job
                CurrentJobMBDone = round(CurrentJobMB - CurrentJobMBLeft)       # Calculate how much has been downloaded
                CurrentJobProgress = round(((CurrentJobMBDone / CurrentJobMB) * 100),2)  # Calculate percentage downloaded
                AnswerStringCurrentDownload = AnswerStringCurrentDownload + 'Progress: %s%% (%s MB / %s MB)\n' % (CurrentJobProgress,  CurrentJobMBDone,  CurrentJobMB)
                            
                # Output to the AnswerObject
                SabnzbdAnswerCurrentDownload = AnswerObject(title='Currently Downloading:',lines=[AnswerObjectLine(text=AnswerStringCurrentDownload)]) 
                
                # --- Queue Details ---
                #Get the items left in the queue           
                AnswerStringQueuedItems = ''
                Count = 0
                for job in jsonDecoded['jobs']:
                    Count = Count + 1
                    AnswerStringQueuedItems = AnswerStringQueuedItems +  str(Count) + ". " + job['filename'] + '\n'
                           
                # Output to the Answer Object
                SabnzbdAnswerQueuedItems = AnswerObject(title='Downoad Queue:',lines=[AnswerObjectLine(text=AnswerStringQueuedItems)]) 
                
                
                # --- Results ---
                #Display the results
                view1 = 0
                view1 = AnswerSnippet(answers=[SabnzbdAnswerQueueStats, SabnzbdAnswerCurrentDownload, SabnzbdAnswerQueuedItems])
                view.views = [view1]
                self.sendRequestWithoutAnswer(view)
                self.complete_request()
            else:
                self.say("There is nothing currently queued for download.")
                self.complete_request()
                
        except (urllib2.URLError):
            self.say("Sorry, a connection to Sabnzbd+ could not be established.")
            self.complete_request()
                
    # ------------------------------------------
    # - Pause Sabnzbd+  -
    # -------------------------------------------
    @register("en-US", "(sab|sabnzbd|download|downloads) (pause|stop)")
    def sab_pause(self, speech, language):
        SabnzbdURL = 'http://%s:%s/sabnzbd/api?mode=pause&output=json&apikey=%s' % (IPAddress,  Port,  APIKey)
        try:
            jsonResponse = urllib2.urlopen(SabnzbdURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            if jsonDecoded['status'] == True:
                self.say("Sabnzbd+ has been paused.")
                self.complete_request()   
            else:
                self.say("Oops! Something went wrong. Please try the command again.")
                self.complete_request()   
            
        except (urllib2.URLError):
            self.say("Sorry, a connection to Sabnzbd+ could not be established.")
            self.complete_request()   
        
    # ------------------------------------------
    # - Resume Sabnzbd+  -
    # -------------------------------------------
    @register("en-US", "(sab|sabnzbd|download|downloads) (resume|unpause|start)")
    def sab_resume(self, speech, language):
        SabnzbdURL = 'http://%s:%s/sabnzbd/api?mode=resume&output=json&apikey=%s' % (IPAddress,  Port,  APIKey)
        try:
            jsonResponse = urllib2.urlopen(SabnzbdURL).read()
            jsonDecoded = json.JSONDecoder().decode(jsonResponse)
            
            if jsonDecoded['status'] == True:
                self.say("Sabnzbd+ has been unpaused.")
                self.complete_request()   
            else:
                self.say("Oops! Something went wrong. Please try the command again.")
                self.complete_request()   
            
        except (urllib2.URLError):
            self.say("Sorry, a connection to Sabnzbd+ could not be established.")
            self.complete_request()       
