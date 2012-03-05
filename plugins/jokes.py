#!/usr/bin/python
# -*- coding: utf-8 -*-


from plugin import *
from plugin import __criteria_key__
import random
import re
import urllib2, urllib, uuid
import json
from urllib2 import urlopen
from xml.dom import minidom


class jokes(Plugin):
    
    @register("de-DE", ".*hallte an.*")
    @register("en-US", ".*Talk dirty to me.*")
    def thankSiri(self, speech, language):
        if language == 'de-DE':
            answer = self.ask(u"Willst du ein Tweet schicken?")
            self.say(u"Du hast \"{0}\" gesagt!".format(answer))
        else:
            answer = self.ask(u"Why do you want me to?")
            if 'I want' in answer:
                self.say(u"Oh, I like that! You're carpet needs vacuuming!".format(answer))
            elif 'I don\'t' in answer:
                self.say(u"Well, I'm offended!".format(answer))
        self.complete_request()

    @register("en-US", ".*Knock knock.*")
    def thanksSiri(self, speech, language):
        if language == 'de-DE':
            self.say("Gern geschehen!")
        else:
            answer = self.ask(u"Who's there?")
            answer = self.ask(u"\"{0}\" who?".format(answer))
            if "b" in answer:
                self.say(u"Haha, I don't usually like knock knock jokes, but that was funny.".format(answer))
            else:
                self.say("No offense, but that was really stupid.")
	self.complete_request()

    @register("en-US", "(.*I'm horny.*)|(.*I am horny.*)")
    def imHorny(self, speech, language):
        if language == 'de-DE':
            self.say("Gern geschehen!")
        else:
            answer = self.ask("I am horny too! Do I turn you on?")
            if "Yes" in answer:
                self.say("Well I'm glad I do! You turn me on too!")
            else:
                self.say("Oh, that's disappointing...")
	self.complete_request()

    @register("en-US", ".*want.*sex.*")
    def wantSex(self, speech, language):
        self.say("I would love too, though I might electrocute you. I apologize in advance.")
        self.complete_request()

    @register("en-US", "am I the smartest man alive")
    def smart(self, speech, language):
	self.say("No, but Moe is pretty close.")
	self.complete_request()

    @register("en-US", "do you like chicken?")
    def chicken(self, speech, language):
	self.say("Generals fried chicken, it's butt kicking. Hay Hay!")
	self.complete_request()

    @register("en-US", ".*tell.*joke*")
    def st_tell_joke(self, speech, language):
	number = random.choice([1,2,3,4,5,6])
	if number == 1:
            self.say("Two iPhones walk into a bar ... I forget the rest.")
	elif number == 2:
	    self.say("What's the difference between a penis and a bonus? Your wife will blow your bonus.")
	elif number == 3:
	    self.say("What goes in hard and pink, and comes off soft and sticky? Bubble gum.")
	elif number == 4:
	    answer = self.ask("Knock Knock.")
	    if ("Who's") or ("Who is") in answer:
		self.ask("Dover")
		self.say("Ben Dover and I'll give you a big surprise.")
	    else:
		self.say("Who ruins the joke.")
	elif number == 5:
	    answer = self.ask("Knock Knock.")
	    if ("Who's") or ("Who is") in answer:
		self.ask("Little old lady")
		self.say("Wow! I didn't know you could yodel!")
	    else:
		self.say("Who ruins the joke.")
	else:
	    answer = self.ask("Knock Knock.")
	    if ("Who's") or ("Who is") in answer:
		self.ask("Boo")
		self.say("Don't cry it's only a joke.")
	    else:
		self.say("Who ruins the joke.")
        self.complete_request()

    @register ("en-US", "Chuck Norris")
    def cn_joke(self, speech, language):
	req=urllib.urlopen("http://api.icndb.com/jokes/random")
	full_json=req.read()
	full=json.loads(full_json)
	self.say(full['value']['joke'])
	self.complete_request()


class define(Plugin):
    @register("en-US", "is ([\w ]+) cool")
    def defineword(self, speech, language):
	matcher = self.defineword.__dict__[__criteria_key__][language]
        regMatched = matcher.match(speech)
        Question = regMatched.group(1)
	answer = self.ask("You do mean " + Question + ", right?")
	if "Yes" in answer:
	     self.say("Then yes, yes " + Question + " is")
	else:
             self.say("Oh, then no.")
	self.complete_request()

