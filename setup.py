#!python

import os
from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from shutil import copyfile
from datetime import datetime
import filecmp

CONF_DIR = "config_files/" # TODO: use this instead
RABBIT_CONF = "/etc/rabbitmq/rabbitmq.config" 
CONF_FILE = "rabbitmq.config"
CONF_PATH = CONF_DIR + CONF_FILE

def config_linux(revert = False):
    if revert:
        print("### Linux config (revert back)", revert_msg)
        print("method not implemented yet, blame Novin ^_^")
        pass
    else:
        print("### Linux config")
        # check if a config file exists?
        if os.path.isfile(RABBIT_CONF) and filecmp.cmp(RABBIT_CONF, CONF_PATH):
            print("config file is already the same!")
            return
        elif os.path.isfile(RABBIT_CONF): 
            # backup
            print("backing up previous config..")
            copyfile(RABBIT_CONF, CONF_PATH + "_bak_" + \
                    datetime.now().strftime("%d%b%Y_%H%M%S"))
        # copy file
        print("copying 'rabbitmq.conf' to /etc/rabbitmq/ ...")
        copyfile(CONF_PATH, RABBIT_CONF)

    print("configuration finished.")



def config_windows():
    print("### Windows config")
    print("method not implemented yet, blame Hannes or Sofia ^_^")
    pass

def config_macintosh():
    print("### Macintosh config")
    print("method not implemented yet, blame Ian ^_^")
    pass


if __name__ == "__main__":
    # TODO: currently this script is only applicable running sudo on linux 
    # TODO: write the argument handling
    # cleanup
    # reverse
    # regular configuration

    # Parsing arguments
    parser = ArgumentParser(description="Applies the configurations required \
                    for the project. Basically only the rabbitmq config file! ")
    parser.add_argument('-c','--cleanup', help='remove temporary files and backups')
    parser.add_argument('-r', '--reverse', help='put the old config file in place')
    args = parser.parse_args()

    if os.name == "posix":
        config_linux()
    elif os.name == "nt":
        config_windows()
    else:
        config_macintosh()

