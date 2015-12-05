#!/bin/sh

# Simple script that will download todays news stories and run the pipeline on it.
# You could set a chron job to run this once a day.

python topstories.py && python parsehtml.py && python synonyms.py
