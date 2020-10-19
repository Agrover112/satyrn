import getopt
import argparse
import multiprocessing
import os
import sys
import time
import webbrowser

from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

from .app import create_app
from .interpreter import Interpreter


def delayed_browser_open(openurl, port):
    time.sleep(3)

    webbrowser.open("http://" + openurl + ":" + str(port) + "/#loaded")


def start_ui(url, port, interpreter, quiet, language):
    openurl = "localhost" if url == "0.0.0.0" else url

    if not quiet:
        print("Booting CherryPy server...")

    d = PathInfoDispatcher({'/': create_app(interpreter, language)})
    server = WSGIServer((url, port), d)

    try:
        p = multiprocessing.Process(target=delayed_browser_open, args=(openurl, port))
        p.start()

        if not quiet:
            print("Hosting at http://" + openurl + ":" + str(port) + "/#loaded")

        server.start()
    except KeyboardInterrupt:
        if not quiet:
            print("Stopping CherryPy server...")

        server.stop()

        if not quiet:
            print("Stopped")


def start_cli(interpreter):
    interpreter.run()


def main():
    interpreter = Interpreter()
    cli_mode = False
    url = "0.0.0.0"
    port = 20787
    language = "english"

    arguments = sys.argv[1:]

    quiet = False

    for opt in arguments:
        if opt == "cli":
            cli_mode = True
        if opt == "ui":
            cli_mode = False
        if opt in ("q", "quiet", "-q", "--quiet"):
            quiet = True

    if not quiet:
        with open(os.path.abspath(__file__)[:(-1 * len(os.path.basename(__file__)))] + "/asciiart.txt") as asciiart:
            print("".join(asciiart.readlines()))

        print("Thank you for using Satyrn! \nFor issues and updates visit https://GitHub.com/CharlesAverill/satyrn")
        print("Documentation is available at https://satyrn.readthedocs.io\n")

    if cli_mode:
        start_cli(interpreter)
    else:
        #opts, args = getopt.getopt(arguments, "pl:hq", ["port=", "lang=", "hidden", "quiet"])
        parser=agrparse.ArgumentParser() 
        parser.add_argument("-p","--port")
        parser.add_argument("-h", "--hidden")
        parser.add_argument("-l", "--lang")
        args=parser.parse_args()
        #argsdict=vars(args)
        #args,leftovers=parser.parse_known_args()
        if args.port:
            if len(args.port) <5:
                port=int(args.port)
            else:
                port=int(p[1:])

        if args.hidden:
            url="127.0.0.1"
        if args.language:
            language=args.language
            
        start_ui(url, port, interpreter, quiet, language)
