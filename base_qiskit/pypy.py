# code developed from James Wootton's Procedural Terrain Generation and Eric Ndirangu's Procedural generation
import argparse
import random
from qiskit import *         
from math import pi
import numpy as np


def get_coordinates( pos, seed=10 ):
    
    (x,y) = pos
    
    qc = QuantumCircuit(2,2)

    for j in range(seed):
        qc.ry(x*pi/seed,0)
        qc.ry(y*pi/seed,1)
        qc.cx(0,1)
    
    qc.measure(0,0)
    qc.measure(1,1)

    counts = execute(qc,Aer.get_backend('qasm_simulator')).result().get_counts()

    for output in ['00', '10', '11', '01']:
        if output not in counts:
            counts[output] = 1

    coordinates = [counts['00'],counts['11'],counts['10'], counts['01']]
    length = np.sqrt( coordinates[0]**2 + coordinates[1]**2 + coordinates[2]**2 + coordinates[3]**2)
    coordinates = [ coordinates[1]**3/length, coordinates[3]**2/length]
    
    return coordinates

g = get_coordinates((2,3))
print(g)
