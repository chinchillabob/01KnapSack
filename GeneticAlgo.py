import random

def score(solution, object_values, object_weights, knapSack):
    value = 0
    weight = 0
    i = 0
    while i < len(solution):
        if solution[i] == 1:
            value = value + object_values[i]
            weight = weight + object_weights[i]
        i = i + 1
    delta = knapSack - weight
    #when delta is one the punishment for being over knapsack is neglagable
    if (delta < 0):
        v = value/2 - (delta**2)
        if v < 0: return 1 
        else: return v
    else: return value

def eval(g0, knapSack, object_values, object_weights):
    val = []
    wt = []
    x = 0
    while x < len(g0):
        v = 0
        w = 0
        i = 0
        while i < len(g0[0]):
            if(g0[x][i]==1):
                v = v + object_values[i]
                w = w + object_weights[i]
            i = i + 1
        if w > knapSack:
            val.append(0)
            wt.append(w)
        else:
            val.append(v)
            wt.append(w)
        x = x + 1
    return [val, wt]

#child is the vector representation of a solution
#mutation rate 0.0-1.0
#returns the child vector that has a mutation_rate chance of having one random modification
def mutate(child, mutation_rate):
    child_copy = child.copy()
    if (random.random() < mutation_rate):
        idx = random.randrange(len(child))
        child_copy[idx] = (child_copy[idx] + 1) % 2
    return child_copy


def init2(II, starting, mutation_rate):
    g0 = []
    for i in range(II):
        g0.append(mutate(starting, mutation_rate))
    return g0

#init state
#create random strngs that are less than knapSack
def init(II, object_values):
    gen0 = []
    while len(gen0) < II:
        s = []
        i = 0
        while i < len(object_values):
            s.append(random.randint(0,1))
            i = i + 1
        gen0.append(s)
    return gen0

#p1 p2 are the one hot encoding repersentation of the parent knapsacks
#returns a list which contains two vectors where each vector repersents one offspring
def reproduce(p1, p2):
    mid = int(len(p1)/2)
    c1 = p1[:mid] + p2[mid:]
    c2 =  p2[:mid] + p1[mid:]
    return [c1, c2]


#returns a list wich repersents the vector of the probaility window for each solution
#ex [.2,.35,.9,.99,1.0]
def sum_prob(prob):
    l = [prob[0]]
    i = 1
    while i < len(prob):
        l.append(l[i-1]+prob[i])
        i = i + 1
    return l

#example output [[1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1], [1, 
#1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]]
def next_gen(parents, II, mutation_rate):
    i = 0
    g1 = parents.copy()
    while i+1 < len(parents):
        p1 = parents[i]
        p2 = parents[i+1]
        children = reproduce(p1, p2)
        g1.append(mutate(children[0], mutation_rate))
        g1.append(children[1])
        i = i + 2
    return g1


#return a list of parents
def selectParents(g0, scores, II):
    p = []
    length_p = 0
    scores = sum_prob(scores)
    r = random.random()
    while (length_p < II/2):
        parent_idx = sum((x < r) for x in scores) 
        if g0[parent_idx] in p:
            r = random.random()
        else:
            p.append(g0[parent_idx])
            r = random.random()
            length_p = length_p + 1
    return p

def train(iter, max_iter, g0, knapSack, II, object_values, object_weights, best_state, bestEval, mutation_rate=1):
    if iter >= max_iter:
        return best_state
     
    scores = []

    for p in g0: 
        scores.append(score(p, object_values, object_weights, knapSack))
    
    max_scores = max(scores)
    if max_scores > bestEval:
        bestEval = max(scores)
        best_state = g0[scores.index(max_scores)]

    scores = [float(i)/sum(scores) for i in scores]
    parents = selectParents(g0, scores, II)
    g1 = next_gen(parents, II, mutation_rate)
    del scores
    return train(iter + 1, max_iter, g1, knapSack, II, object_values, object_weights, best_state, bestEval, mutation_rate)

#knapSack = 100#size of knapsack
#weights = [1, 3, 4, 10, 15, 24, 30, 50, 98, 99]
#values = [1, 1, 1, 2, 2, 4, 4, 7, 14, 14]
#II = 8 #number of permutations to have at each time step t even numbers only
#tmpSolution = [0,0,0,0,0,0,0,0,0,0]
#solution = train(0, 990, init2(II, tmpSolution, 1), knapSack, II, values, weights, tmpSolution, .5)
#print(solution)
#print(eval([solution], knapSack, values, weights)[0][0])