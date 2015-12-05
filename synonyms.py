#!/usr/bin/python

from datetime import date
import os, pickle, sys
from nltk.wsd import lesk
from nltk import pos_tag, word_tokenize
from nltk.stem import LancasterStemmer, RegexpStemmer
from nltk.stem.porter import PorterStemmer
from commonwords import commonwords
import enchant

st = LancasterStemmer()
st2 = RegexpStemmer("ing$|s$|e$|able$",min=4)
st3 = PorterStemmer()
d = enchant.Dict("en_US")

copula = ["be","am","is","are","being","was","were","been"]

def match_suffix(word,lemma,stemmer):
    stem = stemmer.stem(word)
    suff = word[len(stem):]
    lemstem = stemmer.stem(lemma)
    suffix2 = lemma[len(lemstem):]
    lemtest = lemstem + suff
    if d.check(lemtest):
        return lemtest,True
    else:
        return lemma,False

def run_stemmers(word,lemma):
    lemtest,check = match_suffix(word,lemma,st)
    if check:
        return lemtest
    else:
        lemtest,check = match_suffix(word,lemma,st2)
        if check:
            return lemtest
    return lemma
    
def word_synonyms(word, sentence):
    synset = lesk(sentence, word)
    if synset is None:
        return None
    lemmas = synset.lemmas()
    lemmas = [str(lemma.name()) for lemma in lemmas]
    return lemmas

def min_common_synonym(word, sentence):
    synonyms = word_synonyms(word,sentence)
    if synonyms is None:
        return None

    lemma = None
    minlength = None
    for syn in synonyms:
        if syn in commonwords and (minlength is None or len(syn) < minlength):
            lemma = syn
            minlength = len(syn)
    if lemma is None:
        return None
    return lemma

def match_case(reference, lemma):
    if reference == reference.title():
        lemma = lemma.title()
    elif reference == reference.upper():
        lemma = lemma.upper()
    return lemma

def simplify_words(tokenized):
    result = []
    for w in tokenized:
        if w in commonwords or st.stem(w) in commonwords or st2.stem(w) in commonwords or st3.stem(w) in commonwords:
            result.append(w)
            continue

        syn = min_common_synonym(w, tokenized)
        if syn is None:
            result.append(w)
            continue

        lemma = run_stemmers(w,lemma)
        lemma = match_case(w, lemma)

        #lemma = lemma+"("+w+")"
        result.append(lemma)
    return result


def simplify_verbs(tokenized):
    result = []
    pos = pos_tag(tokenized)
    for word,tag in pos:
        if word in commonwords:
            result.append(word)
            continue
        
        if tag[0] != "V":
            result.append(word)
            continue

        syn = min_common_synonym(word, tokenized)
        if syn is None:
            result.append(word)
            continue

        syn = run_stemmers(word,syn)
        syn = match_case(word, syn)

        #syn = syn+"("+word+")"+"[" +tag+ "]"
        result.append(syn)
    return result
    

directory = "news/" + str(date.today())
if not os.path.exists(directory) or not os.path.exists(directory+"/results.p"):
    sys.stderr.write("NEWS DIRECTORY AND DATA NOT FOUND. RUN topstories.py.\n")
    exit()

articles = pickle.load(open(directory+"/results.p", "r"))
url = articles[0]["url"]
filename = url.split("/")[-1].split(".")[0]
if not os.path.exists(directory + "/" + filename + ".txt"):
    #if os.path.exists(directory+"/results.p"):
    #    os.remove(directory+"/results.p")
    sys.stderr.write("NEWS ARTICLES NOT FOUND. RUN parsehtml.py.\n")
    exit()

articles = pickle.load(open(directory+"/results.p", "r"))
for article in articles:
    url = article["url"]
    filename = url.split("/")[-1].split(".")[0]
    path = directory + "/" + filename + ".txt"

    for line in open(path, "r"):
        tokenized = word_tokenize(line)
        line = simplify_verbs(tokenized)
        #line = simplify_words(tokenized)
        print " ".join(line)
    break
