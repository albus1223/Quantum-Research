from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import math
import qiskit.quantum_info as qi

def gate(theta, circuit, i):
    #something is definitely wrong with this gate
    #0 and 360 inputs yield different results
    gate = qi.Operator([[math.cos(theta),-1*(math.sin(theta))], [math.sin(theta),math.cos(theta)]])
    circuit.unitary(gate, i, label = "custom")

simulator = AerSimulator()
qc = QuantumCircuit(1,1)
gate(0, qc, 0)
qc.measure(0, 0)
compiled_circuit = transpile(qc, simulator)
job = simulator.run(compiled_circuit, shots=1000)
result = job.result()
counts = result.get_counts(compiled_circuit)
random_numbers = list(counts.keys())
print(random_numbers)
plot_histogram(counts)


plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.title('1-Qubit RNG')
plt.show()
