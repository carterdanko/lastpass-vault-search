import subprocess
import sys
from workflow import Workflow


def get_password(wf):
    if wf.args:
        vault_id = wf.args[0]
    else:
        vault_id = None

    processed_info = dict()
    lp_show = '/usr/local/bin/lpass show {}'.format(vault_id)
    raw_info = subprocess.check_output(lp_show, shell=True)
    for row in raw_info.split():
        try:
            if row.split(":")[0] == 'Username' or row.split(":")[0] == 'Password':
                processed_info[row.split(":")[0]] = row.split(":")[1]
        except:
            None

    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(processed_info.get('Password').encode('utf-8').strip())

if __name__ == "__main__":
    wf = Workflow()
    sys.exit(wf.run(get_password))
