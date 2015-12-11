Allegory
========

Takes news stories and replaces the real people and places into fictional people and places.


Dependencies:

1. New York Times API
   * Make an account at the new york times developers page
   * Get a key at: http://developer.nytimes.com/docs/reference/keys
   * Put your key in secret.py

2. ARKref coreference engine:
   * http://www.ark.cs.cmu.edu/ARKref/
   * Install the ARKref system and set it up such that the command "arkref.sh" can be called from this directory.
   * For me this involved editing the paths found in the "arkref.sh" scripts, and making symlinks from the arkref.sh script and the arkref/config/ directory to this directory.


