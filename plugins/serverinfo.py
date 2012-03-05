#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import date
import locale 
from plugin import *

class talkToMe(Plugin):   
    
    @register("de-DE", "(Welcher Tag.*)|(Welches Datum.*)")
    @register("en-US", "(What Day.*)|(What.*Date.*)")
    @register("en-GB", "(What Day.*)|(What.*Date.*)")
    @register("fr-FR", u"(Quel jour.*)|(Quel.*date.*)")
    def ttm_say_date(self, speech, language):
        now = date.today()
        if language == 'de-DE':
            locale.setlocale(locale.LC_ALL, 'de_DE')
            result=now.strftime("Heute ist %A, der %d.%m.%Y (Kalenderwoche: %W)")
            self.say(result)
        elif language == 'fr-FR':
            # I have only belgian locale with utf-8... so let Python find the most appropriate for us
            locale.setlocale(locale.LC_ALL, '')
            result=now.strftime(u"Aujourd'hui, nous sommes le %A, %d %m %Y.")
            self.say(result)
        else:
            locale.setlocale(locale.LC_ALL, 'en_US')
            result=now.strftime("Today is %A the %d.%m.%Y (Week: %W)")
            self.say(result)
        self.complete_request()
