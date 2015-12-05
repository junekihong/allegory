#!/usr/bin/python

import os,sys,pickle,re
from pprint import pprint

from datetime import date
from topstories import directory
from characters import *

directory = "news/" + str(date.today())
results = pickle.load(open(directory+ "/results.p", "r"))
filenames = []
"""
for article in results:
    url = article["url"]
    filename = url.split("/")[-1].split(".")[0] + ".tagged"
    filenames .append(filename)
    if not os.path.exists(directory + "/" + filename):
        sys.stderr.write(".tagged FILES NOT FOUND. RUN ARKREF COREF ON THE NEWS ARTICLES\n")
        exit()
"""
for subdir, dirs, files in os.walk(directory):
    for file in files:
        filepath = subdir + os.sep + file
        if filepath.endswith(".tagged"):
            filenames.append(filepath)




def extractID(mentiontag):
    _,mentionid,entityid = mentiontag.split()
    mentionid = mentionid.split("=")[1].strip("\"")
    mentionid = int(mentionid)
    entityid = entityid.split("=")[1][:-1].strip("\"").split("_")
    entityid = tuple([int(x) for x in entityid])
    return mentionid, entityid







regex = re.compile("\<.*?mention.*?\>")


for filename in filenames:
    coref,entities = {},{}
    document = []
    for line in open(filename,"r"):
        line = line.strip()
        #matches = regex.match(line)
        splitted = regex.split(line)
        findall = regex.findall(line)
        """
        #splitted = [x.strip() for x in splitted if x.strip()]
        print " ".join(splitted)
        """
        for tag,text in zip(findall,splitted[1:]):
            if "mentionid" in tag:
                mentionid, entityid = extractID(tag)
                entities[mentionid] = text
                coref[entityid] = coref.get(entityid,[])
                coref[entityid].append(text)
                #print extractID(tag),text


    for line in open(filename, "r"):
        resultline = []
        #line = line.strip()
        splitted = regex.split(line)
        findall = regex.findall(line)
        
        resultline.append(splitted[0])
        for tag,text in zip(findall,splitted[1:]):
            status = True

            """
            test = False
            if "Japan" in text:
                print text
                test = True
            """
            
            while status:
                text,status = direct_match(text)

            """
            if test:
                print text    
            """
            
            if "mentionid" in tag:
                mentionid, entityid = extractID(tag)

                cluster = coref[entityid]
                text = coref_match(text, cluster)
                resultline.append(text)
            else:
                resultline.append(text)
        document.append(" ".join([x.strip() for x in resultline if x.strip()]))

    #print document
    #pprint(coref)
    #pprint(entities)    
    #print "-"*80

    newfilename = filename.split(".")[:-1]
    newfilename = ".".join(newfilename) + ".coreplaced"
    f = open(newfilename,"w")
    f.write("\n".join(document))
    f.close()
