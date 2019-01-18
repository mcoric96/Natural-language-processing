import re
import math
from test_v06 import *
classes = ['AFRIKA','AUSTRALIJA','AZIJA','EUROPA','JUZNA_AMERIKA','SJEVERNA_AMERIKA']#croatian names for continents

def read_file(filename):
    return open(filename, 'r', encoding='utf-8').read()

#first we read file,create unigram model(dictionary) of that document,countries in text are separated with " "
def file_to_doc_model(filename):
    d = {} #dictionary-unigram model of a given text
    l = [w.lower() for w in read_file(filename).strip().split()]
    #iterating on list of countries
    for country in l:
        if country in d:
            d[country.lower()]+=1
        else:
            d[country.lower()]=1
    return d

#build learning model , input: path - path of folder which contains training examples. Each folder is 1 class(continent) and contains
#documents with names of countries. Output : trained model - dictionary with classes(continents - Africa,Europe,...) as keys and list of documents
#from that particular class turned into unigram model
def build_train_model(path):
    import os
    train_model = {}
    for folder in os.listdir(path):
        train_model[folder] = []
        for filename in os.listdir(path + folder + '/'):
            train_model[folder].append(file_to_doc_model(path + folder + '/' + filename))
    return train_model

TRAIN_PATH = 'train/'
TEST_PATH = 'test/'
train_model = build_train_model(TRAIN_PATH)#dictionary,key is the name of the continent,value is a list of unigrams

#input: trained model from function build_train_model
#output: prior is a dictionary with classes as keys and their prior probabilities as values.For each class c: P(c) = Nc / N where Nc is
#number of documents of class c and N is number of all documents from training set
def get_prior(train_model):
    d = {} #prior probabilities
    n = 0 #number of all documents
    for continent in classes:
        n += len(train_model[continent])
    for continent in classes:
        d[continent] = len(train_model[continent])/n
    return d

#input: trained model from function build_train_model
#output: megadoc_model is dictionary with classes as keys and mega-document(concatenation of all documents of particular class c) are values
def get_megadoc_model(train_model):
    d = {} #returned value,dicntionary
    for continent in train_model.keys():
        c_dict = {} #dictionary for 1 continent
        for d1 in train_model[continent]: #for each unigram(dictionary) of 1 continent
            for k in d1.keys():
                if k in c_dict:
                    c_dict[k] += d1[k]
                else:
                    c_dict[k] = d1[k]
        d[continent] = c_dict
    return d

#input: megadoc_model from function get_megadoc_model,output: set of all words from all megadocuments
def get_vocabulary(megadoc_model):
    l = []
    for continent in megadoc_model.keys():
        for country in megadoc_model[continent]:
            l.append(country)
    return set(l)

#input: megadoc_model and test_model represented as unigram
#output:conditional probability P(w|c)(with add-1 smoothing) for all words from test model per each class
# P(c|w) = (|(w,C)|+1) / (|C|+|V|) where C is set of all classes and V is complete vocabulary
def get_likelihood(megadoc_model, test_model):
    #for dictionary megadoc_model, keys are classes(continents) and values are dictionaries with countries as keys,each with number of showing up
    #in that unigram as values    test model is unigram with countries as keys and number of showing up as values
    continents = megadoc_model.keys()
    n = len(get_vocabulary(megadoc_model)) #length of vocabulary
    d = {} # unigram - dictionary
    for continent in continents:
        num_classes = 0
        for country in megadoc_model[continent]:
            num_classes += megadoc_model[continent][country]
        for country in test_model.keys():
            #for each continent and each country, we compute pobability that country belongs to that continent
            #we sum up all apperances of that country in unigram(dictionary) of that continent
            #we sum up all words in megadoc of that particular class(continent)
            num = 0
            if country in megadoc_model[continent].keys():#ako se drzava ijednom "pojavila" u kontinentu
                num = megadoc_model[continent][country]
            p = (num+1)/(num_classes+n) #P(w|c) likelihood
            d[(country,continent)] = p
    return d

#input:likelihood of conditional probability P(w|c) , test model as unigram,prior probability od classes
#conditional probabilities P(c|d) that document d is in the class c. Its is represented with dictionary,such that classes are keys and P(c|d)
#probabilities are values. P(c|d) = P(c)*P(c|w1)*...*P(c|wn) for all words w1,...,wn from vocabulary V.
#For this problem we use log-space because probabilities are very small numbers. logP(c|d) = logP(c)+logP(c|w1)+...+logP(c|wn)
def get_posterior(prior, likelihood, test_model):
    d = {} #dictionary
    for continent in classes:
        posterior = math.log(prior[continent])#probability od class(continent)
        for key in likelihood.keys():
            if key[1] == continent:
                posterior += math.log(likelihood[key])
        d[continent] = round(posterior,5)
    return d

#input:trained model and test model from files , output: the most probable continent(class)
def classify(train_model,test_model):
    megadoc = get_megadoc_model(train_model) #megadoc model from training set
    prior = get_prior(train_model)#dictionary of prior probabilities for classes
    likelihood = get_likelihood(megadoc,test_model)#conditional probabilities for test model
    posterior = get_posterior(prior,likelihood,test_model)#posterior probabilities for test model
    #from posterior probabilities ,we choose class with the biggest posterior probability
    c = classes[0]
    for i in range(1,len(classes)):
        if posterior[classes[i]] > posterior[c]:
            c=classes[i]
    return c
