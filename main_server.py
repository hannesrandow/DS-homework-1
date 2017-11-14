"""
Starter Script for Sudoku server
"""

from argparse import ArgumentParser # Parsing command line arguments
from sys import path,argv
from os.path import abspath, sep
from sudoku.server.server import server_main

# Client Info -------------------------------------------------------------------
___NAME = 'Sudoku Server'
___VER = '0.1'
___DESC = 'An awesome Sudoku server'
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
    parser.add_argument('-f', '--filename', help='the name of the sudoku',
                        action='store_true', default='sudoku_easy_1')
    args = parser.parse_args()


    # Run server awesome
    server_main(args)