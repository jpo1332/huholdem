#!/usr/bin/env python3
from subprocess import call
import sys

version = sys.argv[1]
verstion = str(version)
call(["python",  "flopdata{0}.py".format(version)])
call(["python",  "turndata{0}.py".format(version)])
call(["python",  "riverdata{0}.py".format(version)])
call(["python",  "nnprocess.py", "flopnn{0}data.csv".format(version), "flopnn{0}data1.csv".format(version)])
call(["python",  "nnprocess.py", "turnnn{0}data.csv".format(version), "turnnn{0}data1.csv".format(version)])
call(["python",  "nnprocess.py", "rivernn{0}data.csv".format(version), "rivernn{0}data1.csv".format(version)])
#call("ls")
