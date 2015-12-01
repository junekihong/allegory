#!/usr/bin/python
#commonwords contains the 1000 most common words, and its titled capitalization: about, About, apple, Apple, etc

# Taken from: http://splasho.com/upgoer5/phpspellcheck/dictionaries/1000.dicin
f = open("1000.commonwords")
words = [x.strip() for x in f.readlines()]
words = [x for x in words] + [x.title() for x in words]
commonwords = sorted(words)

