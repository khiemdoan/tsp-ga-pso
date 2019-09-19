import logging
import sys

import gi
gi.require_version('Gtk', '3.0')

from application import Application


APP_ID = 'com.daugau.TSP-GA-PSO'

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app = Application(APP_ID)
    app.run(sys.argv)
