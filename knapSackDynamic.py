def knapSack(W, wt, val): 
    n=len(val)
    table = [[0 for x in range(W + 1)] for x in range(n + 1)] 
    solution = [0]*n
    for i in range(n + 1): 
        for j in range(W + 1): 
            if i == 0 or j == 0: 
                table[i][j] = 0
            elif wt[i-1] <= j: 
                table[i][j] = max(val[i-1]  
+ table[i-1][j-wt[i-1]],  table[i-1][j]) 
            else: 
                table[i][j] = table[i-1][j] 
   
    return table[n][W] 

#knapSackSize = 100
#weights = [1, 3, 4, 10, 15, 24, 30, 50, 98, 99]
#values = [1, 1, 1, 2, 2, 4, 4, 7, 14, 14]

#print(knapSack(knapSackSize, weights, values))