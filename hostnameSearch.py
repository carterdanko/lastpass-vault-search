import subprocess
import re
import sys
from collections import defaultdict
from fuzzywuzzy import process
from workflow.workflow import Workflow

# vaultMap = dict()
vault_map = defaultdict(list)


def get_host_ids(wf):

    if wf.args:
        query = wf.args[0]
    else:
        query = None

    vault_raw = subprocess.check_output('/usr/local/bin/lpass ls', shell=True)

    for row in vault_raw.split('/'):
        if row != '(none)':
            try:
                hostname = row.split(' [id: ')[0]
                host_id = re.sub('[^0-9]', '', row.split(' [id: ')[1])
                add_to_local(hostname, host_id)
            except:
                None

    hostname_lookup(query)


def add_to_local(hostname, host_id):
    vault_map[hostname].append(host_id)


def hostname_lookup(hostname):
    results = process.extract(hostname, vault_map.keys(), limit=5)
    # spits back the top five results, this will have to be relayed to the workflow and then user selected
    # once it does we have the key for the map and we can get the id.

    # topChoice = some user choice always going to be results[X][0] for the index in the list of
    # tuples and then the str and not the length
    for iter_host in results:
        for host_id in vault_map.get(iter_host[0]):
            lp_show = '/usr/local/bin/lpass show {}'.format(host_id)
            raw_info = subprocess.check_output(lp_show, shell=True)
            username = 'NO USERNAME'
            url = ''
            if "Username" in raw_info and "URL" in raw_info:
                username = raw_info.split('\n')[1].split('Username:')[1].strip()
                url = raw_info.split('\n')[3].split('URL:')[1].strip()
            wf.add_item(title=iter_host[0],
                        subtitle=username+'    '+url,
                        arg=host_id,
                        icon='icon.png',
                        valid=True)

    wf.send_feedback()

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(get_host_ids))
