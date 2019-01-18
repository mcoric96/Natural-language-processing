#function is using matrix of min distance,we are searching for minimum number of operations (deleting,throw-in,substitution) of letters
#to translate one string into another
#Levensthein algorithm
def str_distance(string1,string2):
    if type(string1) != str or type(string2) != str:
        print('Wrong argument type!')
        return
    if len(string1) == '' or len(string2) =='':
        print('Enter at least one letter for each string!')
        return
    #if all arguments are good
    n = len(string1)
    m = len(string2)
    mx = [[0 for j in range(m+1)] for i in range(n+1)]
    #first values
    for i in range(0,n+1):
        mx[i][0] = i
    for j in range(0,m+1):
        mx[0][j] = j
    #second values
    for i in range(1,n+1):
        for j in range(1,m+1):
            a = 2 if string1[i-1] != string2[j-1] else 0
            mx[i][j] = min(mx[i-1][j]+1 , mx[i][j-1]+1 , mx[i-1][j-1] + a)
    return (mx[n][m],mx)

#backtrace alignment algorithm for 2 strings,this alingment is not unique in some cases,it depends on letters in strings,somethimes
#there is more than one good alignment
def align(string1,string2):
    matrix = str_distance(string1.lower(),string2.lower())[1] # we need to have matrix of distances for backtracking
    n , m = len(string1) , len(string2)
    word1 = ''
    word2 = ''
    #backtracking starts at (n,m) point in matrix
    i , j = n , m #indices for backtracking
    while i >= 1 or j >= 1: #algorithm stops when we reach (0,0) point in matrix
        if string1[i-1].lower() == string2[j-1].lower(): # if those 2 letters are equal,diagonal
            word1 = string1[i-1] + word1
            word2 = string2[j-1] + word2
            i = i-1
            j = j-1
        else: #2 different letters
            #first we want to check if we can go to this field diagonally(substitution)
            if (matrix[i-1][j-1] + 2) == matrix[i][j]: #2 different letters
                word1 = string1[i-1] + word1
                word2 = string2[j-1] + word2
                i = i-1 #we move diagonally in the matrix
                j = j-1
            elif (matrix[i][j-1] + 1) == matrix[i][j]: #we are returning left,deleting action
                word1 = '-' + word1
                word2 = string2[j-1] + word2
                j = j-1 #we move left in the matrix
            else: #if we are returning down,throw-in new letter
                word1 = string1[i-1] + word1
                word2 = '-' + word2
                i = i-1 #we move down in the matrix
    return (word1,word2)
