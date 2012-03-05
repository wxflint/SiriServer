#!/usr/bin/python
# -*- coding: utf-8 -*-
#Made by Maxx
#Thanks to JimmyKane and his debug level 9 for the siriproxy (<333) and Eichhoernchen for
#making the python siriserver
#Credits to gaVRos for some minor adjustments and testing

import re
import logging
import time
import pytz

from datetime import *
from pytz import timezone
from uuid import uuid4
from plugin import *

from siriObjects.baseObjects import *
from siriObjects.uiObjects import *
from siriObjects.systemObjects import *
from siriObjects.emailObjects import *

class checkEmail(Plugin):

	#Command to activate the checking of email...
	@register("en-US","(.*email.*)|(.*mail.*)")
	@register("en-GB","(.*email.*)|(.*mail.*)")
	def emailSearch(self, speech, language):

		#Let user know siri is searching for your mail GOOD!
		view_initial = AddViews(self.refId, dialogPhase="Reflection")
		view_initial.views = [AssistantUtteranceView(text="Let me check your mail...", speakableText="Let me check your mail...", dialogIdentifier="EmailFindDucs#findingNewEmail")]
		self.sendRequestWithoutAnswer(view_initial)
		
		#Grabs the timeZone given by the client
		tz = timezone(self.connection.assistant.timeZoneId)
		
		#Search object to find the mail GOOD!
		email_search = EmailSearch(self.refId)
		email_search.timeZoneId = self.connection.assistant.timeZoneId
		email_search.startDate = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=tz)
		email_search.endDate = datetime.now(tz)
		email_return = self.getResponseForRequest(email_search)
		email_ = email_return["properties"]["emailResults"]
		if email_return == []:
			view = AddViews(self.refId, dialogPhase="Summary")
			view.views += [AssistantUtteranceView(text="Looks like you don't have any email.", speakableText="Looks like you don't have any email.", dialogIdentifier="EmailFindDucs#foundNoEmail")]
			self.sendRequestWithoutAnswer(view)
		else:
			self.logger.warning(email_return)

			#Display the mail! It works :D!
			view = AddViews(self.refId, dialogPhase="Summary")
			view1 = AssistantUtteranceView(text="Ok, here is what I found: ", speakableText="Ok, here is what I found: ", dialogIdentifier="EmailFindDucs#foundEmail")
			snippet = EmailSnippet()
			snippet.emails = email_
			view2 = snippet
			view.views = [view1, view2]
			self.sendRequestWithoutAnswer(view)
		self.complete_request()