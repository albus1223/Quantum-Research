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
    print("len(random_numbers): ",len(random_numbers))
    init_occ = 0
    numbs_below_max = []
    for i in range(0, len(random_numbers)):
        if int(binarytodecimal(random_numbers[i])) <=maximum:
            init_occ = init_occ + counts[random_numbers[i]]
            numbs_below_max.append(random_numbers[i])

    x = shot_count  - init_occ
    print("initial occ sum is ", init_occ)
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

            print("binary_new_number: ", binary_new_number)
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
    return numbs_below_max2


numbs, occ = rng(360, 60, 9)



def rng2(maximum, rng, shot_count, qubit_count):


    gate = qi.Operator([[,], [,]])

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
    print("len(random_numbers): ",len(random_numbers))
    init_occ = 0
    numbs_below_max = []
    for i in range(0, len(random_numbers)):
        if int(binarytodecimal(random_numbers[i])) <=maximum:
            init_occ = init_occ + counts[random_numbers[i]]
            numbs_below_max.append(random_numbers[i])

    x = shot_count  - init_occ
    print("initial occ sum is ", init_occ)
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

            print("binary_new_number: ", binary_new_number)
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
    return numbs_below_max2
