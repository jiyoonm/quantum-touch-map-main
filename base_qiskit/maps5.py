from qiskit import QuantumCircuit, execute, Aer, QuantumRegister
from math import pi
import random

from qc_tools import plot_height

import numpy as np


def make_line ( length ):
    # determine the number of bits required for at least `length` bit strings
    n = int(np.ceil(np.log(length)/np.log(2)))
    # start with the basic list of bit values
    line = ['0','1']
    # each application of the following process double the length of the list,
    # and of the bit strings it contains
    for j in range(n-1):
        # this is done in each step by first appending a reverse-ordered version of the current list
        line = line + line[::-1]
        # then adding a '0' onto the end of all bit strings in the first half
        for j in range(int(len(line)/2)):
            line[j] += '0'
        # and a '1' onto the end of all bit strings in the second half
        for j in range(int(len(line)/2),int(len(line))):
            line[j] += '1'
    return line


line = make_line(8)
print(line)


def make_grid(L):
    
    line = make_line( L )
    
    grid = {}
    for x in range(L):
        for y in range(L):
            grid[ line[x]+line[y] ] = (x,y)
    
    return grid


grid = make_grid(8)



def height2circuit(height,grid):
    
    n = len( list(grid.keys())[0] )
        
    state = [0]*(2**n)
    
    H = 0
    for bitstring in grid:
        (x,y) = grid[bitstring]
        if (x,y) in height:
            h = height[x,y]
            state[ int(bitstring,2) ] = np.sqrt( h )
            H += h
        
    for j,amp in enumerate(state):
        state[ j ] = amp/np.sqrt(H)
                
    qc = QuantumCircuit(n,n)
    qc.initialize( state, qc.qregs[0] )
        
    return qc


def circuit2height(qc,grid,backend,shots=None,log=False):
    
    # get the number of qubits from the circuit
    n = 8
    # construct a circuit to perform z measurements
    meas = QuantumCircuit(n,n)
    for j in range(n):
        meas.measure(j,j)
        
    # if no shots value is supplied use 4**n by default (unless that is too small)
    if not shots:
        shots = max(4**n,8192)

    #run the circuit on the supplied backend
    counts = execute(qc+meas,backend,shots=shots).result().get_counts() 
    
    # determine max and min counts values, to use in rescaling
    if log: # log=True uses the log of counts values, instead of the values themselves
        min_h = np.log( 1/10 ) # fake small counts value for results that didn't appear
        max_h = np.log( max( counts.values() ) )
    else:
        min_h = 0
        max_h = max( counts.values() )   
    
    # loop over all bit strings in `counts`, and set the corresponding value to be
    # the height for the corresponding coordinate. Values are rescaled to ensure
    # that the biggest height is 1, and that no height is less than zero.
    height = {}
    for bitstring in counts:
        if bitstring in grid:
            if log: # log=True uses the log of counts values, instead of the values themselves
                height[ grid[bitstring] ] = ( np.log(counts[bitstring]) - min_h ) / (max_h-min_h)
            else:
                height[ grid[bitstring] ] = ( counts[bitstring] - min_h ) / (max_h-min_h)
    
    return height


def generate_seed(L,num=5):
    # generate a height map of `num` randomly chosen points, each with randomly chosen values
    seed = {}
    for _ in range(num):
        x = random.randint(0,L-1)
        y = random.randint(0,L-1)
        seed[x,y] = random.random()
    # set one to have a height of exactly 1
    seed[random.choice(list(seed.keys()))] = 1
        
    return seed

L = 16
grid = make_grid(L)
seed = generate_seed(L)

qc = height2circuit(seed,grid)
qc.ry((pi/32),qc.qregs[0])

tartan = circuit2height(qc,grid,Aer.get_backend('qasm_simulator'),log=True)
plot_height(tartan,color_map='gray',op_path='moviefilein5', file_name='test5.png')
