from __future__ import unicode_literals
import sys
import hostnameSearch
import usernameSearch
import utility
from workflow.workflow import Workflow

wf = Workflow()

def main(wf):

    utility.precheck()

    if len(wf.args) == 1:
        query = wf.args[0]
    elif len(wf.args) > 1:
        lookup_by, query = wf.args
    else:
        query = None

    # if 'upgrade' in query:
    #     utility.parse_utility('upgrade')
    #     sys.exit(0)

    if query in ('--updateCache', '-U'):
        utility.parse_utility('update_cache')
        sys.exit(0)
    else:
        if lookup_by == 'hostname':
            hostnameSearch.hostname_lookup(query)
        elif lookup_by == 'username':
            usernameSearch.username_lookup(query)


def send_feedback():
    wf.send_feedback()

if __name__ == u"__main__":
    sys.exit(wf.run(main))