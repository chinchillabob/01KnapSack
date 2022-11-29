import GeneticAlgo as GA
import knapSackDynamic as DA
import matplotlib.pyplot as plt
import time
import random

def generateWtVal(knapSack, length):
    i = 0
    weights = []
    values = []
    while i < length:
        w = random.randint(0, knapSack)
        v = int(random.uniform(0.8, 1.2)*w)
        weights.append(w)
        values.append(v)
        i = i + 1
    return [weights, values]

def run(maxObjects, knapSack, II):
    l = 5
    timeGa = []
    timeDyn = []
    lengths = []
    ga_vals = []
    max_vals = []
    correct = 0
    loss_val = 0
    while l + 1 < maxObjects:
        wv = generateWtVal(knapSack, l)
        w = wv[0]
        v = wv[1]
        startingState = [0]*len(w)
        start = time.time()
        solution = GA.train(0, 200, GA.init2(II, startingState, 1), knapSack, II, v, w, startingState, .5)
        end = time.time()
        timeGa.append(end-start)
        solutionValue = GA.eval([solution], knapSack, v, w)[0][0]
        start = time.time()
        m = DA.knapSack(knapSack, w, v)
        end = time.time()
        max_vals.append(m)
        timeDyn.append(end-start)
        lengths.append(l)
        ga_vals.append(solutionValue)
        if m == solutionValue: correct = correct + 1
        l = l + 2
        #print(f"iter: {l}")
    print("Percentage correct: {}".format(correct/maxObjects))
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.plot(lengths, timeGa, label="GA")
    ax1.plot(lengths, timeDyn, label="DYN")
    ax2.plot(lengths, ga_vals, label="GA")
    ax2.plot(lengths, max_vals, label="DYN")
    plt.legend()
    plt.show()


knapSack = 1000#size of knapsack
II = 8
run(500, knapSack, II)