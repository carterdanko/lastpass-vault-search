import subprocess
import sys
from workflow import Workflow


def parse_arguments(wf):
    if wf.args:
        action, vault_id = wf.args
    else:
        vault_id = None

    if vault_id == "lpass-cli_login":
        subprocess.check_output('/usr/bin/osascript TerminalLoginLaunch', shell=True)
        sys.exit(1)

    processed_info = dict()
    lp_show = '/usr/local/bin/lpass show {}'.format(vault_id)
    raw_info = subprocess.check_output(lp_show, shell=True)
    for row in raw_info.split('\n'):
        try:
            if row.split(":")[0] == 'Username' or row.split(":")[0] == 'Password':
                processed_info[row.split(":")[0]] = row.split(":")[1]
        except:
            None

    if action == 'getPassword':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processed_info.get('Password').encode('utf-8').strip())
    elif action == 'getUsername':
        process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(processed_info.get('Username').encode('utf-8').strip())

if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(parse_arguments))
