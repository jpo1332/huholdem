#!/usr/bin/env python3
from subprocess import call
import sys

version = sys.argv[1]
verstion = str(version)
call(["python",  "nn{0}.py".format(version), "flopnn{0}data1.csv".format(version),
      "flopmodel{0}.ckpt".format(version)])
call(["python",  "nn{0}.py".format(version), "turnnn{0}data1.csv".format(version),
      "turnmodel{0}.ckpt".format(version)])
call(["python",  "nn{0}.py".format(version), "rivernn{0}data1.csv".format(version),
      "rivermodel{0}.ckpt".format(version)])
#call("ls")
