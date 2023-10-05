import math
import matplotlib.pyplot as plt
import qiskit.quantum_info as qi
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

#Define function to convert a string from binary to decimal
def binarytodecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal

#Define gate with matrix:
#                       [(1/np.sqrt(2), (1/np.sqrt(2)]
#                       [(1/np.sqrt(2), (-1/np.sqrt(2)]
#       aka Hadamard Gate
gate = qi.Operator([[(1/np.sqrt(2)), (1/np.sqrt(2))], [(1/np.sqrt(2)), (-1/np.sqrt(2))]])

print(gate)

#Create simulator object
simulator = AerSimulator()

#Initialize quantum circuit with 2 qubits and 2 cbits
qc = QuantumCircuit(2, 2)

#Apply "gate" to quantum Circuit
#[0, 1] Ensures it is applied to both qubits
qc.unitary(gate, [0, 1], label="Haddy Daddy")

#Measure the first and second qubits,
#then map them to the first and second cbits
qc.measure([0,1],[0,1])

#Run simulator, etc.
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1)
result = job.result()
counts = result.get_counts(compiled_circuit)

#Print out the number
print("Random Number: ", binarytodecimal(list(counts.keys())[0]))
