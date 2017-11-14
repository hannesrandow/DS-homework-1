"""
This is the main script for the client.
It calls all the necessary scripts on the client side
"""

from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
from sudoku.client.clientgui import client_gui_main
from sudoku.client.clientterminal import client_terminal_main

# Client Info -------------------------------------------------------------------
___NAME = 'Sudoku Client'
___VER = '0.1'
___DESC = 'An awesome Sudoku client'
___BUILT = '07-11-2017'
___VENDOR = 'Teamwork'


def __info():
    return '%s version %s (%s) %s' % (___NAME, ___VER, ___BUILT, ___VENDOR)
# -------------------------------------------------------------------------------


if __name__ == '__main__':
    # Find the script absolute path, cut the working directory
    a_path = sep.join(abspath(argv[0]).split(sep)[:-1])
    # Append script working directory into PYTHONPATH
    path.append(a_path)

    # Parsing arguments
    parser = ArgumentParser(description=__info(), version = ___VER)
    parser.add_argument('-t','--terminal', help='run terminal client', action='store_true')
    parser.add_argument('-g', '--gui', help='run gui client', action='store_true')
    args = parser.parse_args()

    # Run client awesome
    if args.gui:
        #Run application with GUI
        client_gui_main(args)
    else:
        #Run application from terminal
        client_terminal_main(args)