from __future__ import unicode_literals
import vault_search
from fuzzywuzzy import process
from workflow.workflow import Workflow

wf = Workflow()
UPDATE_INTERVAL = 3600 * 3
localCache = wf.cached_data('usernameList')


def username_lookup(username):
    if not wf.cached_data_fresh('usernameList', max_age=UPDATE_INTERVAL) or wf.cached_data('hostIdList') is None:
        vault_search.update_caches()
    match_found = localCache.get(str(username))
    if match_found < 1:
        results = process.extract(username, localCache.keys(), limit=3)
        fuzzy_match(results, username)
    else:
        exact_match(match_found, username)

    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.


def fuzzy_match(results, username):
    for bad_variable_name in results:
        info = localCache.get(bad_variable_name[0])
        host_id = info[0][0]
        hostname = info[0][1]
        wf.add_item(title=bad_variable_name[0],
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=host_id,
                    icon='icon.png',
                    valid=True)

    send_feedback()


def exact_match(match_found, username):
    for info in match_found:
        host_id, hostname = info
        wf.add_item(title=hostname,
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=host_id,
                    icon='icon.png',
                    valid=True)

    send_feedback()


def send_feedback():
    wf.send_feedback()
