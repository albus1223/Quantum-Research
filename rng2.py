from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt





def binarytodecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal


def rng(maximum, shot_count):
    simulator = AerSimulator()


    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(6, 6)


    # Add a H gate on qubit 0
    for i in range(0, 6):
        circuit.h(i)


    # Map the quantum measurement to the classical bits
    for i in range(0,5):
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
            new_circ = QuantumCircuit(6, 6)
            for j in range(6):
                new_circ.h(j)
            new_circ.measure([0, 1], [0, 1])
            new_circ.measure([2, 3], [2, 3])
            new_circ.measure([4, 5], [4, 5])
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
