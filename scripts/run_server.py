#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tallypi.webapp.routes import application
from bottle import run

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 7413))
	run(application, server='paste', reloader = False, host = '0.0.0.0', port = port, quiet = False)
	application.close()
