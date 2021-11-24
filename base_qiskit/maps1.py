from qiskit import QuantumCircuit, Aer, execute
from math import pi
from qc_tools import plot_height

from random import random
import matplotlib.pyplot as plt
from matplotlib import cm

L = 15
project_dir = project.folder
file_name ='base_qiskit/test.png'
file_path = '{}/{}'.format(project_dir, file_name)

def get_height(x,y):
    
    qc = QuantumCircuit(1,1)
    
    # perform rotations, whose angles depend on x and y
    qc.x(0)
    # low frequency rotations to create island shape
    qc.rx((1/32)*x*pi,0) 
    qc.ry((1/32)*y*pi,0)
    
    # perform a z measurement
    qc.measure(0,0)
    
    # determine the probability of a 1
    try:
        p = execute(qc,Aer.get_backend('qasm_simulator'),shots=10000).result().get_counts()['1']/1000
    except:
        p = 0
    
    # return p^2 as the height
    return p**3

z = [ [get_height(x,y) for x in range(-L,L)] for y in range(-L,L) ]\
    
def plot_z(z,L):
    
    fig, ax = plt.subplots()
    fig.set_size_inches(L/2,L/2)
    cs = ax.contourf(z,25,cmap=cm.get_cmap('gray'))

    plt.axis('off')
    plt.savefig(file_path, bbox_inches='tight')

    plt.show()
    op('moviefilein1').par.file =file_path
    op('moviefilein1').par.reloadpulse.pulse()

    
plot_z(z,L)