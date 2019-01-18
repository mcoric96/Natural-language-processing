#simple spelling checker,we can use this functions to check spelling in some text by generating possible corrections

#input: word , output: all words such that we deleted exactly 1 letter from input word
def deletes(word):
    l = []
    a = len(word)
    for i in range(0,a):
        w = ""
        for j in range(0,a):
            if j != i:
                w += word[j]
        lista.append(w)
    return set(l)

#input: word and a string which represents some alphabet ,for example : 'abcdxy',for every letter of the word and every letter of the alphabet
#we add letter to every possible , place in the word,for exaple: word='dog',alphabet='ab' => output is { adog,daog,doag,doga,bdog,dbog,dobg,dogb }
def inserts(word, alphabet):
    l = []
    for letter in alphabet:
        l.append(word+letter)
        l.append(letter+word)
        for i in range(0,len(word)-1):
            l.append(word[0:i+1]+letter+word[i+1:])
    return set(l)

#input: word and a string which represents some alphabet , example : 'abcdxy' , for every letter of the word 'x' and every letter of alphabet 'y'
#we substitue current letter 'x' of the word for letter 'y'
def replaces(word, alphabet):
    l=[]
    a = len(word)
    for letter in alphabet:#for each letter in alphabet
        l.append(letter+word[1:])
        l.append(word[0:a-1]+letter)
        for i in range(1,a-1):
            l.append(word[0:i]+letter+word[i+1:])
    return set(l)

#input: word , for every 2 neighbor letters,we switch them
def transposes(word):
    l = []
    l.append(word[1]+word[0]+word[2:])
    for i in range(1,len(word)-1):
        l.append(word[0:i]+word[i+1]+word[i]+word[i+2:])
    return set(l)

#input: word and alphabet , we return all words such that edit-distance between them and word at the beggining is 1
def edits1(word, alphabet):
    return deletes(word) | replaces(word,alphabet) | inserts(word,alphabet)| transposes(word)

#input:word,alphabet,model(unigram model - dictionary,words are key,their frequencies are values)
def spell_candidates(word, alphabet, model):
    list1 = edits1(word,alphabet) & set(model) #intersection of all words which edit-distance from the word is 1 and all words from unigram model
    l = []
    for k in list1:#new list with pairs(frequency,candidate)
        l.append((model[k],k))
    l=sorted(l,reverse = True) #we sort words by frequency from given unigram model
    a = []
    for pair in l:
        a.append(pair[1])
    return a
