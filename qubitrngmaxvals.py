from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt





def binarytodecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal


def rng():
    shots = 0
    simulator = AerSimulator()


    # Create a Quantum Circuit acting on the q register
    circuit = QuantumCircuit(6, 6)


    # Add a H gate on qubit 0
    for i in range(6):
        circuit.h(i)


    # Map the quantum measurement to the classical bits
    circuit.measure([0, 1], [0, 1])
    circuit.measure([2, 3], [2, 3])
    circuit.measure([4, 5], [4, 5])


    # Compile the circuit for the support instruction set (basis_gates)
    # and topology (coupling_map) of the backend
    compiled_circuit = transpile(circuit, simulator)


    # Execute the circuit on the aer simulator
    job = simulator.run(compiled_circuit, shots=60)


    # Grab results from the job
    result = job.result()


    # Returns counts
    counts = result.get_counts(compiled_circuit)
    random_numbers = list(counts.keys())
    print("len(random_numbers): ",len(random_numbers))


    numb_decimal = []
    occurrences = []

    for i in range(0, len(random_numbers)):
        shots = shots+1
        maximum = 51
        numb = binarytodecimal(random_numbers[i])

        if numb < maximum:
            numb_decimal.append(numb)
            occurrence = counts[random_numbers[i]]
            occurrences.append(occurrence)
        elif numb > maximum:
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

            print("binary_new_number: ", binary_new_number)


            # Search if that number already exists
            if binary_new_number < maximum:
                if binary_new_number in numb_decimal:
                    occurrences[numb_decimal.index(binary_new_number)] += 1
                else:
                    numb_decimal.append(binary_new_number)
                    occurrences.append(1)



    return numb_decimal, occurrences, shots


numbs, occ, shots = rng()


print("numbs: ",numbs)
print("occ: ",occ)
print("numbs len: ",len(numbs))
print("occ len",len(occ))
print("occ sum: ", sum(occ))
print("Shots: ", shots)


plt.plot(numbs, occ, linewidth=1)


plt.xlabel('Number')
plt.ylabel('Occurrences')
plt.title('10-Qubit RNG')
plt.show()
