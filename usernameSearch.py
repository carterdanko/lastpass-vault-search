from __future__ import unicode_literals
import subprocess
import re
import sys
import main
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

wf = Workflow()
UPDATE_INTERVAL = 3600 * 3
localCache = wf.cached_data('usernameList')

def usernameLookup(username):
    if not wf.cached_data_fresh('usernameList', max_age=UPDATE_INTERVAL) or wf.cached_data('hostIdList') == None:
        main.updateCaches()
    matchFound = localCache.get(str(username))
    if matchFound < 1:
        results = process.extract(username, localCache.keys(), limit=3)
        fuzzyMatch(results, username)
    else:
        exactMatch(matchFound, username)

    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.


def fuzzyMatch(results, username):
    for badvariablename in results:
        info = localCache.get(badvariablename[0])
        hostId = info[0][0]
        hostname = info[0][1]
        wf.add_item(title=badvariablename[0],
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=hostId,
                    icon='icon.png',
                    valid=True)

    sendFeedback()

def exactMatch(matchFound, username):
    for info in matchFound:
        hostId=info[0]
        hostname=info[1]
        wf.add_item(title=hostname,
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=hostId,
                    icon='icon.png',
                    valid=True)

    sendFeedback()

def sendFeedback():
    wf.send_feedback()
