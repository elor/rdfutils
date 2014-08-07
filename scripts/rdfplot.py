#!/usr/bin/env python

import corporate_design
corporate_design.set_layout(layout_type='beamer', size='big')
from rdfutils import read_file, bond_length, smoothen, coordination_length
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import sys
import re
from subprocess import call

if not len(sys.argv) > 1:
    print("""Not enough arguments.
    Syntax: %s <file.rdf>..."""%sys.argv[0])
    exit(1)

for filename in sys.argv[1:]:
#    print "reading %s"%filename
    rdf = read_file(filename)
    smooth = smoothen(rdf, 0.1)
    
    bondlength = bond_length(smooth)
    coordinationlength = coordination_length(smooth)
#    coordination = coordination_number(smooth)
#    print("%s: %s"%(filename, bondlength))
#    print("%s: %s"%(filename, coordinationlength))
#    print("%s: %s"%(filename, coordination))

    plt.plot(rdf[0], rdf[1], '-', color='black', label="%s raw"%re.sub(r'^([0-9]*K).*$', r'\1', re.sub(r'_', r'\_', filename)))
    
    plt.axvline(x=bondlength, color='red')
    plt.axvline(x=coordinationlength, color='red')

#    ymax = max([max(smooth[1]), max(rdf[1])])
    plt.plot(smooth[0], smooth[1], '-', color='green', label="%s smooth"%re.sub(r'^([0-9]*K).*$', r'\1', re.sub(r'_', r'\_', filename)))
#    plt.plot(smooth[0], [s/ymax for s in smooth[1]], '-', label="%s smooth"%re.sub(r'^([0-9]*K).*$', r'\1', filename))
plt.legend()
#plt.show()

#ax=plt.axes()
#ax.xaxis.set_major_formatter (FormatStrFormatter("%3.1f"))
#ax.yaxis.set_major_formatter (FormatStrFormatter("%3.2f"))

plt.savefig('smoothrdf.pdf')
plt.close()
call(["pdf2png.sh", "smoothrdf.pdf"])

