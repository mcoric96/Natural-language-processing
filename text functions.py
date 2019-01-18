import re

def read_file(filename):#read file
    return open(filename,"r",encoding = "utf8").read()

def count_chars(text,chars): #number of specific characters in the text
    br = 0
    for ch in text:
        if ch in chars:
            br+=1
    return br

def count_subtext(text,subtext,case_sensitive):
    br=0
    l=len(subtext) #length of subtext
    for i in range(0,len(text)-len(subtext)+1):
        if case_sensitive == False:
            if text[i:i+l].lower() == subtext.lower():
                br+=1
        else:
            if text[i:i+l] == subtext:
                br+=1
    return br

#this function returns a number of time pattern shows up in text
def count_patter(text,pattern):
    return len(re.findall(pattern,text))

#primitive function return a list of all words in the text using regular expressions
def all_words(text):
    return re.findall(r'\w+',text)

#this function return all upper words in the text
def upper_words(text):
    return re.findall(r'\b[A-ZŠĐČĆŽ][A-Za-zŠĐČĆŽšđčćž]*',txt)

#this function return all words with some specific subtext 'infix'
def match_infix(text,infix):
    return re.findall(r'\b[A-Za-zČĆŽŠĐšđčćž]*'+infix+r'[a-zšđčćž]*\b',txt)

#this function return a list of PHONE numbers in the text like  xxxx-xxx or xxx-xxx or 063 675 887 or 09766512345,but not 'regular' numbers
#like 768-897 or 435 893
def phone_regex(text):
    return re.findall(r'[+]?[0-9]{1,5}[ -.]?[0-9]{3,4}[ -.]?[0-9]{3,4}',text)

#this function return a list of emails in text,most emails like xxxxxxx@xxxxxx.yyy x are letters ,numbers or #$-_  and y are letters
#email should not start with number or signs -+.#$,it should start with letter... emails like abcd@.com or -3@abcd.com are not valid
def email_regex(text):
    return re.findall(r'\b[a-zA-Z]{1,}[a-zA-Z0-9#$_\-\.]*@[a-zA-Z0-9#%\-\._]+\.[a-zA-Z]{1,5}\b',text)

#this function return a dictionary(distribution of words),with lenghts of words as keys and number of words of each length as it's values
def words_len_dist(text):
    if type(text) != str:
        return
    words = all_words(text)
    d = dict()
    for w in words:
        if len(w) in d:
            d[len(w)]+=1
        else:
            d[len(w)]=1
    return d

def split_text(text,sep): #split text by given subtext (separator)
    a=len(sep)
    lista=[]
    izraz=""
    index=0
    while index < len(text)+1:
        if len(text[index:]) < a: #if we can finish algorithm
            izraz+=text[index:]
            lista.append(izraz)
            break
        if text[index:index+a] == sep:
            lista.append(izraz)
            izraz = ""
            index+=a
        else:
            izraz+=text[index]
            index+=1
    if lista[0] == "":
        lista=lista[1:]
    if lista[len(lista)-1] == "":
        lista=lista[:len(lista)-1]
    return lista

# this function return number of appearances of word "word" in the text
def word_freq(text,word,case_sensitive):
    #if type(text) != str or type(word) != str or case_sensitive != bool:
        #return
    count=0
    l=all_words(text)# first we collect all words in the text
    for a in l:
        if case_sensitive:
            if a == word:
                count+=1
        else:
            if a.lower() == word.lower():
                count+=1
    return count
