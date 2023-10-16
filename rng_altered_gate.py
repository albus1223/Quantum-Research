from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import math
import qiskit.quantum_info as qi





def binarytodecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal

def gate(theta, circuit, i):
    gate = qi.Operator([[math.cos(theta),-1*(math.sin(theta))], [math.sin(theta),math.cos(theta)]])
    circuit.unitary(gate, i, label = "custom")


def rng(maximum, shot_count):
    simulator = AerSimulator()

    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(1, 1)

    theta_input = int(input("theta: "))
    # Add a H gate on qubit 0
    for i in range(1):
        gate(theta_input, circuit, i)


    # Map the quantum measurement to the classical bits
    circuit.measure([0], [0])
    #circuit.measure([0, 1], [0, 1])
    #circuit.measure([2, 3], [2, 3])


    # Compile the circuit for the support instruction set (basis_gates)
    # and topology (coupling_map) of the backend
    compiled_circuit = transpile(circuit, simulator)


    # Execute the circuit on the aer simulator
    job = simulator.run(compiled_circuit, shots=shot_count)


    # Grab results from the job
    result = job.result()


    # Returns counts
    counts = result.get_counts(compiled_circuit)
    random_numbers = list(counts.keys())
    init_occ = 0
    numbs_below_max = []
    for i in range(0, len(random_numbers)):
        if int(binarytodecimal(random_numbers[i])) <=maximum:
            init_occ = init_occ + counts[random_numbers[i]]
            numbs_below_max.append(random_numbers[i])

    x = shot_count  - init_occ
    numb_decimal = []
    occurrences = []

    for i in range(0, len(numbs_below_max)):
        occurrences.append(counts[numbs_below_max[i]])

    for i in range(0,x):
        while True:
            newsim = AerSimulator()
            # Create a new circuit
            new_circ = QuantumCircuit(1, 1)
            for j in range(1):
                new_circ.h(j)
            new_circ.measure([0], [0])
            #new_circ.measure([0, 1], [0, 1])
            #new_circ.measure([2, 3], [2, 3])
            #new_circ.measure([4, 5], [4, 5])
            compiled_new_circ = transpile(new_circ, newsim)
            new_job = newsim.run(compiled_new_circ, shots=1)
            output = new_job.result()

            new_result = output.get_counts(compiled_new_circ)
            new_number = list(new_result.keys())[0]

            binary_new_number = binarytodecimal((new_number))

            if binary_new_number <= maximum:
                break

        # Search if that number already exists
        if binary_new_number <= maximum:
            if binary_new_number in numbs_below_max:
                occurrences[numbs_below_max.index(binary_new_number)] += 1
            else:
                numbs_below_max.append(binary_new_number)
                occurrences.append(1)

    numbs_below_max2 = []
    for i in range(0, len(numbs_below_max)):
        numbs_below_max2.append(binarytodecimal(str(numbs_below_max[i])))
    return numbs_below_max2, occurrences


numbs, occ = rng(50, 1000)

rng_dict = {}

for i in range(0, len(numbs)):
    if numbs[i] in rng_dict:
        rng_dict[numbs[i]] += occ[i]
    else:
        rng_dict[numbs[i]] = occ[i]


plt.bar(numbs, occ, linewidth=1)


plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.title('10-Qubit RNG')
plt.show()
