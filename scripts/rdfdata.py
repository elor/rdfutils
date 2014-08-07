#!/usr/bin/env python

from rdfutils import *
import sys

if not len(sys.argv) > 1:
    print("""Not enough arguments.
    Syntax: %s <file.rdf>..."""%sys.argv[0])
    exit(1)

print("#filename\tbondlength\tcoordination\tcoord.length\tN-density")

for filename in sys.argv[1:]:
    raw = read_file(filename)
    smooth = smoothen(raw, 0.1)
    print("%s\t%f\t%f\t%f\t%f"%(filename, bond_length(smooth), coordination_number(smooth), coordination_length(smooth), get_rho(raw)))
