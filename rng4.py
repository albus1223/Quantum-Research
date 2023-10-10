import math
import matplotlib.pyplot as plt
import qiskit.quantum_info as qi
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


#QRNGs are used to generate random gates for the main QRNG. How stackable is this?


def binarytodecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal


def rng(maximum, shot_count, qubit_count):

    #SPECIFY DOMAIN FOR RNG

    simulator = AerSimulator()


    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(qubit_count, qubit_count)


    # Add a H gate on qubit 0
    for i in range(qubit_count):
        circuit.h(i)


    # Map the quantum measurement to the classical bits
    for i in range(0, qubit_count-1):
        circuit.measure([i, i+1], [i, i+1])


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
            new_circ = QuantumCircuit(qubit_count, qubit_count)
            for j in range(qubit_count):
                new_circ.h(j)
            for i in range(0, qubit_count-1):
                new_circ.measure([i, i+1], [i, i+1])
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
    print(numbs_below_max2[0])
    return numbs_below_max2[0]

def rounder(number, decimalPlaces):
    return float(int(number * (10 ** decimalPlaces))) / 10 ** decimalPlaces


def rng2(maximum, shot_count, qubit_count):

    theta = rng(90, 10, 7)
    #one random value for whole matrix
    gate = qi.Operator([[math.cos(theta), math.sin(-theta)], [math.sin(theta), math.cos(theta)]])

    print(gate)

    simulator2 = AerSimulator()


    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(qubit_count, qubit_count)


    # Add a H gate on qubit 0
    for i in range(qubit_count):
        circuit.unitary(gate, [i], label="Haddy Daddy")


    # Map the quantum measurement to the classical bits
    for i in range(0, qubit_count-1):
        circuit.measure([i, i+1], [i, i+1])


    # Compile the circuit for the support instruction set (basis_gates)
    # and topology (coupling_map) of the backend
    compiled_circuit = transpile(circuit, simulator2)


    # Execute the circuit on the aer simulator
    job = simulator2.run(compiled_circuit, shots=shot_count)


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
            newsim2 = AerSimulator()
            # Create a new circuit
            new_circ = QuantumCircuit(qubit_count, qubit_count)
            for j in range(qubit_count):
                new_circ.unitary(gate, [j], label="Haddy Daddy")
            for i in range(0, qubit_count-1):
                new_circ.measure([i, i+1], [i, i+1])
            compiled_new_circ = transpile(new_circ, newsim2)
            new_job = newsim2.run(compiled_new_circ, shots=1)
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


numbs, occ = rng2(50, 60, 6)

rng_dict = {}

for i in range(0, len(numbs)):
    if numbs[i] in rng_dict:
        rng_dict[numbs[i]] += occ[i]
    else:
        rng_dict[numbs[i]] = occ[i]




plt.plot(numbs, occ, linewidth=1)


plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.title('10-Qubit RNG')
plt.show()
