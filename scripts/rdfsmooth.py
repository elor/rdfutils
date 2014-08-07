#!/usr/bin/env python

from rdfutils import read_file, write_string, smoothen
import sys

if not len(sys.argv) == 2:
    print("""Invalid number of arguments!

Syntax: %s <file.rdf>
"""%sys.argv[0])
    exit(1)

filename = sys.argv[1]
rdf = read_file(filename)
smooth = smoothen(rdf) # with default values
string = write_string(smooth)

print(string)
