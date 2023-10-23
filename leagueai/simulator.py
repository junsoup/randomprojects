import csv
import random
import copy

# def generateSim(row):
#     if not row:
#         return [[]]

#     first_element = row[0]
#     rest_of_elements = row[1:]

#     rest_combinations = generateSim(rest_of_elements)
#     result = []

#     for combination in rest_combinations:
#         result.append([0] + combination)
#         result.append([first_element] + combination)

#     return result

def save(sim):
    # print(sim)
    out = ""
    for simMatch in sim:
        for champ in simMatch:
            out += str(champ) + ','
        out = out[:-1] + '\n'
    with open(r"outSim.txt", 'a') as file:
        file.write(out)

with open('out1.txt', 'r') as file:
    csv_reader = csv.reader(file)
    counter = 1
    finalOut = []
    for row in csv_reader:
        sim = [int(x) for x in row]
        sim += row[:5]
        finalOut.append(sim)
        for _ in range(3):
            sim2 = copy.deepcopy(sim)
            removeNum = random.sample(range(0, 10), random.randint(0, 10))
            for idx in removeNum:
                sim2[idx] = 0
            finalOut.append(sim2)
        print(counter)
        counter += 1
    save(finalOut)


print("Done! Whew that was a lot of work!")
