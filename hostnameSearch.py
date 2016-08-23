from __future__ import unicode_literals
import main
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

vault_map = defaultdict(list)
UPDATE_INTERVAL = 3600 * 3
wf = Workflow()


def hostname_lookup(hostname):
    local_cache = wf.cached_data('hostIdList')
    if not wf.cached_data_fresh('hostIdList', max_age=UPDATE_INTERVAL) or wf.cached_data('hostIdList') is None:
        main.update_caches()
    match_found = local_cache.get(str(hostname))
    if match_found <= 1:
        results = process.extract(hostname, local_cache.keys(), limit=3)
        fuzzy_match(results, hostname)
    else:
        exact_match(match_found, hostname)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.


def fuzzy_match(results, hostname):
    try:
        local_cache = wf.cached_data('hostIdList')
    except:
        fuzzy_match(results, hostname)

    for bad_variable_name in results:
        info = local_cache.get(bad_variable_name[0])
        host_id = info[0][0]
        username = info[0][1]
        wf.add_item(title=bad_variable_name[0],
                    subtitle=username + ' ' + ' \u2318-Click to copy username; ',
                    modifier_subtitles={
                        'cmd': '\u2318-Click to copy username.'
                    },
                    arg=host_id,
                    icon='icon.png',
                    valid=True)

    send_feedback()


def exact_match(match_found, hostname):
    for info in match_found:
        host_id, username = info
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
