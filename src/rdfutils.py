import re as _re
from numpy import convolve as _convolve
from numpy import mean as _mean
from numpy import transpose as _transpose
from math import exp as _exp
from math import pi as _pi
from math import sqrt as _sqrt
import itertools as _itertools

# read a .rdf file and return a 3xN array containing [[radius], [rdf], [coord]]
def read_file(filename):
	file = open(filename)
	return read_lines(file)

# read a single string of the contents of a .rdf file
def read_string(string):
	return read_lines(string.split('\n'))

# read an array of lines of a .rdf file
def read_lines(lines):
	lines = [line.strip().split() for line in lines if not _re.match('^\s*#', line)]
	firstline = lines[0]
	assert(len(firstline) == 2)
	lines = [[float(x) for x in line[1:]] for line in lines[1:]]
	return _transpose(lines)

def write_lines(rdf):
        raise Exception('Not yet implemented', 'This function has not yet been implemented')

def write_string(rdf):
        return '\n'.join(write_lines(rdf))

def write_file(rdf, filename):
        file = open(filename, 'w')
        file.write(write_string(rdf))
        file.close()
        return

# gauss distribution, helper function
def _gauss(x, mu, sigma):
    sigma2 = sigma**2
    return _exp(-(x-mu)**2/sigma2) / _sqrt(2*_pi*sigma2)

# volume of a spherical shell, helper function
def _sphere_shell_volume(r_outer, r_inner):
    return 4.0/3*_pi*(r_outer**3 - r_inner**3)

# get the particle density from a complete set of RDF data
def get_rho(rdf):
    coord = rdf[2]
    rdf = rdf[1]
    rho = _mean([c/r for c,r in zip(coord, rdf) if r > 0.0])
    return rho

# get step width of a proper radius array (no validation)
def get_dr(r):
    dr = (r[-1] - r[0]) / (len(r)-1)
    return dr

# from radius, rdf data and particle density, create and return coordination data
def create_coord(rdf, rho):
    r = rdf[0]
    rdf = rdf[1]
    coord=[0.0]*len(r)
    
    for i in range(1, len(coord)):
        coord[i] = coord[i-1] + (rdf[i]*_sphere_shell_volume(r[i], r[i-1])) * rho
    
    return coord

# smoothen RDF data using a gaussian convolution
def smoothen(rdf, sigma = 0.05):
    rho = get_rho(rdf)
    r = rdf[0]
    rdf = rdf[1]
    dr = get_dr(r)
    sigma /= dr

    width = int(len(rdf)/8)
    pattern = [_gauss(x, width*0.5, sigma) for x in range(0, width)]
    patternweight = sum(pattern)
    pattern = [ x/patternweight for x in pattern ]

    rdf = _convolve(rdf, pattern, 'same')
    ret = [r, rdf, None]
    ret[2] = create_coord(ret, rho)

    return ret

# retrieve the bond length of a smooth RDF function ( = first clear peak above 1.0)
def bond_length(rdf):
    r = rdf[0]
    rdf = rdf[1]
    peaks = [i for i in range(1, len(r)-1) if (rdf[i]-rdf[i-1])*(rdf[i+1]-rdf[i]) < 0.0 and rdf[i]-rdf[i-1] > 0 and rdf[i] > 1.0]

    return r[peaks[0]]
