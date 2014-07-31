#!/usr/bin/env python

import re as _re
import numpy as _np

# returns a 3xN array containing [[radius, rdf, rdf_accumulated]]
def readFile(filename):
	file = open(filename)
	return readStrings(file)

def readString(string):
	return readStrings(string.split('\n'))

def readStrings(strings):
	lines = [line.strip().split() for line in strings if not _re.match('^\s*#', line)]
	firstline = lines[0]
	assert(len(firstline) == 2)
	lines = [[float(x) for x in line[1:]] for line in lines[1:]]
	return _np.transpose(lines)

