#!/usr/bin/python
#By Rabih

import os

def at_uptime():

     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"

     total_seconds = float(contents[0])

     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24

     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )

     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )

     return string;

from plugin import *
class uptime(Plugin):

    @register("en-US", "(.*Uptime.*)|(.*Status.*)|(.*Server.*)")
    def st_uptime(self, speech, language):
        if language == 'en-US':
            self.say("SiriServer has been running " + at_uptime())
        self.complete_request()
