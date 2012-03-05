#!/usr/bin/python                                                                                                                                                                   
# -*- coding: utf-8 -*-  
#by P4r4doX
#for Siri Server
#reports bug to zatovic@azet.sk

import urllib2, nltk, json
from plugins.wikipedia.config import *
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
from plugin import *
from siriObjects.baseObjects import AceObject, ClientBoundCommand
from siriObjects.uiObjects import AddViews, AssistantUtteranceView
from siriObjects.answerObjects import AnswerSnippet, AnswerObject, AnswerObjectLine 


class wikipedia(Plugin):
    @register("en-US", "(.*wikipedia.*)")
    def wiki(self, speech, language):
	#Json search results (via MediaWiki API)
	def searchWiki(lang, query):
		file = urllib2.urlopen("http://%s.wikipedia.org/w/api.php?" % (lang)+
				      urlencode({'action':'opensearch',
						  'search':query,
						  'format':'json',
						  'limit': searchlimit}))
		data = json.load(file)
		return data

	#save results to array 
	def resultsArray(lang, query):
		error = 0
		number = 0
		results = []
		while(error != 1):
			try:
				results.append(searchWiki(lang, query)[1][number])
				number = number + 1
			except IndexError:
				error = 1
		return results
	query = ""
	#ask for user's query
	query = speech.replace('Wikipedia', '',1)
	if (query == ""):
		query = self.ask('What would you like to search ?')

	self.say("Searching ..")
	error = 0
	number = 0
	WikipediaResults = ""
	results = resultsArray(lang, query)
	while (error != 1):
		try:  
			results[number]
			WikipediaResults = WikipediaResults + str(number + 1) + " : " + unicode(results[number]) + "\n"
			number = number + 1
		except IndexError:
			error = 1
	
	if (number == 0):
	  self.say("I didn't find anything !")
	  self.complete_request()
	#show results
	view = AddViews(self.refId, dialogPhase="Completion")
	view1 = 0
	Wikipedia = AnswerObject(title='Results',lines=[AnswerObjectLine(text=WikipediaResults)])
	view1 = AnswerSnippet(answers=[Wikipedia])
	view.views = [view1]
	self.sendRequestWithoutAnswer(view) 
	#ask for article
	invalid = 1
	while(invalid != 0):
		self.say("Answer only number article (one, two, ...)", " ")
		id = self.ask('Which one ?')
		try:
			id = int(id)
		except:
			invalid = 1
			continue
		if(id > number):
			invalid = 1
			continue
		else:
			invalid = 0
	self.say("Checking ...")
	#parse article
	query = str(results[id-1])
	url = "http://%s.wikipedia.org/w/index.php?" % (lang) + urlencode({'action':'render','title':query})
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	html = opener.open(url).read()
	html = str(html)
	paragraph = BeautifulSoup(''.join(html)).findAll('p')
	text = paragraph
	
	#show article
	error = 0
	number = 0
	while (error != 1):
		try:
			text[number]
			number = number + 1
		except IndexError :
			error = 1
	paragraphsCount = number - 1
	lastCount = 10

	WikipediaArticle = ""
	error = 0
	number = 0
	while (error != 1):
		if (number == lastCount):
			error = 1
		try:
			text[number]
			WikipediaArticle = WikipediaArticle + nltk.clean_html(unicode(text[number]))
			number = number + 1
		except IndexError :
			error = 1
	
	view = AddViews(self.refId, dialogPhase="Completion")
	view1 = 0
	Wikipedia = AnswerObject(title=query,lines=[AnswerObjectLine(text=WikipediaArticle)])
	view1 = AnswerSnippet(answers=[Wikipedia])
	view.views = [view1]
	self.sendRequestWithoutAnswer(view) 
	
	
	while (paragraphsCount-lastCount > 0):
		loadmore = self.ask('Would you like to load more ?')
		WikipediaArticle = ""
		if (loadmore == 'Yes'):
		  lastCount = lastCount + 10
		  error = 0
		  while (error != 1):
			  if (number == lastCount):
				  error = 1
			  try:
				  text[number]
				  WikipediaArticle = WikipediaArticle + nltk.clean_html(unicode(text[number]))
				  number = number + 1
			  except IndexError :
				  error = 1
		else:
			self.complete_request()
		view = AddViews(self.refId, dialogPhase="Completion")
		view1 = 0
		Wikipedia = AnswerObject(title=query,lines=[AnswerObjectLine(text=WikipediaArticle)])
		view1 = AnswerSnippet(answers=[Wikipedia])
		view.views = [view1]
		self.sendRequestWithoutAnswer(view)
		
	self.complete_request()