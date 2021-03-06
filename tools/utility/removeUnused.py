import argparse
import os

import time

import math

import tools.utility.log as lo
from tools.utility import messageFactory

LOGGER = lo.get_logger('api')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--remove-dir', type=str,
                        default='.',
                        help='Set path to config file')
    parser.add_argument('--logs-path', type=str,
                        default='.',
                        help='Set path to config file')
    args = parser.parse_args()
    mf = messageFactory.MessageFactory()
    LOGGER.info('Removing unused files')
    to_remove = []
    for root, dirs, files in os.walk(args.remove_dir):
        for fi_name in files:
            with open(args.logs_path, 'r') as f:
                remove = True
                for line in f:
                    if fi_name in line:
                        remove = False
                        break
                if remove:
                    remove_path = '{}/{}'.format(root, fi_name)
                    st = os.stat(remove_path)
                    c_time = st.st_ctime
                    c_time = time.time() - c_time
                    c_time = c_time / 60 / 60 / 24
                    if math.floor(c_time) != 0:
                        to_remove.append(remove_path)
    mf.send_removed_temp_diff_files()
    for remove in to_remove:
        try:
            os.remove(remove)
        except OSError as e:
            mf.send_automated_procedure_failed('Remove unused diff files',
                                               e.message)

