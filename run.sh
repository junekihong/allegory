#!/bin/sh

# Simple script that will download todays news stories and run the pipeline on it.
# You could set a chron job to run this once a day.

python topstories.py && python parsehtml.py #&& python synonyms.py


if [ $? -eq 0 ]; then
    for file in news/*/*.txt
    do
        echo "RUNNING COREF ON: " $file
        ./coref.sh $file 2> /dev/null
    done
fi


if [ $? -eq 0 ]; then
    python coref.py && python synonyms.py
fi
