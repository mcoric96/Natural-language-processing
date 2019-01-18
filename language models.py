import re,random
from nltk.tokenize import regexp_tokenize , sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters# this is for abbrevations
from nltk.data import load
#special non letter symbols
symbols = ['.',',','',' ','!','?','\\','<','>','/','#','$','%','@','&','*','(',')','+','','-','_','=','{','}','[',']','...']
abbrevations = ['u.s.a', 'fig.','dr.','dr.sc.','jan.','aug.','feb.','a.m.','p.m.','a.k.a','c.e.o.','r.i.p'] #example of abbrevations

def read_file(filename):#read file
    return open(filename,"r",encoding = "utf8").read()

def stop_words():#classic list of English stop words
    text = open("data\english.stop","r",encoding = "utf8").read()
    return text.split("\n")

#primitive function for sentence segmentation from text,try it with decision tree for '.'
def segment_sentence(text):
    pattern = r'[.?!]\s*'
    return [sentence.strip("{}[]() ") for sentence in re.split(pattern,text) if sentence != ""]

#using NLTK library for tokenizing all words from english text WORKS THE BEST
def tokenizeWords(text):
    pattern = r'(?:[A-Za-z]{1,3}\.)+|\w+(?:[-\'_]\w+)*|\$?\d+(?:\.\d+)*%?'
    return regexp_tokenize(text,pattern)
    
#using NLTK library,it returns sentences of a given text,preffered for english vocabulary
#(keep nltk.data.load and tokenize module and function !)
def tokenizeText(text):
    sent = load('tokenizers/punkt/english.pickle')
    a = sent.tokenize(text)
    sentences = []
    for s in a:
        sentences.extend(sent_tokenize(s))
    return sentences

def tokenizeText2(text): #for abbrevations
    punkt_param = PunktParameters()
    abbreviation = abbrevations
    punkt_param.abbrev_types = set(abbreviation)
    tokenizer = PunktSentenceTokenizer(punkt_param)
    return[sent for sent in tokenizer.tokenize(text) if sent not in symbols]

#function for words segmentation from given text,words defined only with alpha characters or numbers
def segment_word(text):
    pattern = r"[.?!\n, \'\"#$%@()-=+*&|/]\s*"
    return [word.strip("{}[]() ") for word in re.split(pattern,text) if word != ""]

#function for building ngrams from a given sentence
def build_ngram(sentence,ngram_size):
    words = ['<sent>']
    words.extend(tokenizeWords(sentence))
    words.append('</sent>')
    ngrams = []#list of ngrams
    for i in range(len(words)-ngram_size+1):
        ngrams.append(tuple(words[i:i+ngram_size]))
    return ngrams

#function for building model for given text
#return value is dictionary with ngrams as keys and their number of showing up in the text as values
def build_model(text,ngram_size):
    if text.strip(' ,.:;/?\|#$%*()[]{}<>?@"') == '':
        print('Wrong input')
        return
    text = text.lower()
    dictionary = {}
    sentences = segment_sentence(text) #first we need to have all sentences in the text
    for sent in sentences:
        ngrams = build_ngram(sent, ngram_size) #then we create ngrams for each sentence
        for a in ngrams:  #now we count all ngrams 
            if a in dictionary:
                dictionary[a] +=1
            else:
                dictionary[a] = 1
    return dictionary

#function for building language model using sentence probabilities and digram/unigram model from a function above
#probability of digram (A,B) is ratio of number of (A,B) digrams in text and number od A unigram in text
#function return probability of the sentence using digram model chaining rule  P(w1,...w2) = P(w1)*P(w2|w1)*...*p(wn|wn-1)
def digram_probability(sentence,text): #sentence must be a part of the text! Otherwise the model wont work properly!
    p = 1 #probability of a sentence using n-gram model
    model1 = build_model(text,1) #unigram list from given text
    model2 = build_model(text,2) #digram list from given text
    for digram in build_ngram(sentence,2):
        a = model2[digram] / model1[digram[:1]] #ratio between digrams and unigrams starting with first word of digram
        p = p * a
    return p

#improvement of digram model of language using Laplace k-smoothing
#probability of each digram is calculated by formula P(A,B) = (|(A,B)|+k) / (|A| + k|V|) where is V set of all unigrams in this model
#function return probability of the sentence using digram model chaining rule  P(w1,...w2) = P(w1)*P(w2|w1)*...*p(wn|wn-1)
def digram_prob_laplace(sentence,text,k):
    if type(k) != int:
        print('Wrong input!')
        return
    if k <= 0:
        print('Wrong input!')
        return
    p = 1
    model1 = build_model(text,1) #unigram list from given text
    model2 = build_model(text,2) #digram list from given text
    x = len(model1.keys())
    for digram in build_ngram(sentence,2):
        #we need to check if digram is in model2
        if digram in model2.keys():
            a = (model2[digram]+k) / (model1[digram[:1]]+k*x)
            p = p * a
    return p

#generating random sentences using some language model
def generate_sentence(model):
    word = '<sent>'
    sentence = []
    while word != '</sent>':
        next_ngrams = list({ngram for ngram in model if ngram[0] == word})
        if next_ngrams:
            next_ngram = random.choice(next_ngrams)
            sentence.append(next_ngram)
            word = next_ngram[-1]
            if word == '<sent>':
                break
        else:
            break
    sentence = ' '.join(' '.join(ngram[1:]) for ngram in sentence).strip('</sent>')
    return sentence

def read_model(filename):
    #input: filename - file path , output: language model(dictionary)
    txt = open(filename, 'r', encoding='utf8').read().strip()
    model = {}
    for line in txt.split('\n'):
        if not line.startswith('#'):
            line = line.split('\t')
            ngram, freq = line[:-1][0], int(line[-1])
            model[ngram] = freq
    return model

def write_model(filename, model, comment = None):
    #input: -filename: file path  -model: langauage model   -comment: optional comment on the beggining of the file
    #this function writes model into file, every line of this file will be w1\tw2\tw3\t...\twn\tfreq
    #where w1, ..., wn are words of ngram,freq frequency of each word
    f = open(filename, 'w', encoding='utf8')
    if comment: f.write('# ' + str(comment) + '\n')
    for freq, ngram in sorted(((freq, ngram) for ngram, freq in model.items()), reverse=True):
        f.write('\t'.join(ngram) + '\t' + str(freq) + '\n')
    f.close()
