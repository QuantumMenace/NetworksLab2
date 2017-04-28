"""
Lab 3 Proxy written by Tim Anderson and Dan McGarry
"""

from socket import *
from shutil import copyfile
import os
import sys

if (len(sys.argv) != 2)
	print "Incorrect number of arguments."
	sys.exit(2)

port = int(sys.argv[1])