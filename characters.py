#!/usr/bin/python
import re

characters = {

    # People
    "obama":"Bouba",
    "barack obama": "Bouba the Shapeshifter",
    "hillary":"Lucy",
    "hillary clinton": "Lucy the Fairy Godmother",
    "trump":"Duck",
    "donald trump": "Donald Duck",
    "donald j. trump": "Donald Duck",
    "jeb": "Burt",
    "jeb bush": "Burt the Turtle",
    "bush": "Turtle",
    "john kerry": "Kiki the Sharpie",
    "john": "Kiki",
    "kerry": "Sharpie",
    "mr. xi": "Mr. Freeze",
    "xi": "Freeze",
    "jinping": "Cold",
    "dalai lama": "Daily Llama",
    
    
    # Actors
    #"isis": "Sauron",
    "islamic state": "Sauron",
    "exxon": "Klaxxon",
    "texaco": "Mexacco",

    
    # Places
    "the united states": "Middle-Earth",
    "united states": "Middle-Earth",
    "u.s.": "Middle-Earth",
    "american": "Earthian",
    "american citizens":"Earthians",

    "cuba": "Curopa",
    "cubas": "Curopas",
    "cuban": "Curopean",
    "cubans": "Curopeans",
    "havana": "Banana",
    "castro": "Cantalope",
    
    "russia": "Mars",
    "russian": "Martian",
    "france": "the Moon",
    "french": "Moonish",
    "parisian": "Moonian",
    "paris": "Moon Moon",
    "canada": "the Ice Kingdom",
    "canadian": "Icelandic",
    "morroco": "Marco Polo",
    "china": "Atlantis",
    "chinas": "Atlantises",
    "chinese": "Atlantean",
    "asia": "Oceania",
    "asian": "Oceanic",
    "africa": "Venus",
    "african": "Venetian",
    "britain": "Laputa",
    "british": "Laputian",
    "english": "Laputian",
    "japan": "Jurrasic Park",
    "japanese": "Jussasic",
    "germany": "Jupiter",
    "german": "Jovian",
    "australia": "Caveland",
    "australian": "Cavelandian",
    "south korea": "South Pluto",
    "south korean": "South Plutonian",
    "korean": "Plutonian",
    "north korea": "North Pluto",
    "north korean": "North Plutonian",
    
}


# Taken from: http://www.really-learn-english.com/list-of-pronouns.html
pronouns = [
    "I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "what", "who"
    "me", "whom"
    "mine", "yours", "his", "hers", "ours", "theirs"
    "this", "that", "these", "those"
    "which", "what", "whose", "whoever", "whatever", "whichever", "whomever",
    "myself", "yourself", "himself", "herself", "itself", "ourselves", "themselves",
    "Anything", "everybody", "another", "each", "few", "many", "none", "some", "all", "any", "anybody", "anyone", "everyone", "everything", "no one", "nobody", "nothing", "none", "other", "others", "several", "somebody", "someone", "something", "most", "enough", "little", "more", "both", "either", "neither", "one", "much", "such"
]
pronouns = list(set([x.lower() for x in pronouns]))


def match_case(x, reference):
    if reference == reference.upper():
        return x.upper()
    if reference == reference.title():
        return x.title()
    if reference == reference.lower():
        return x.lower()
    return x

def coref_match(text, cluster):
    if text.lower() in pronouns:
        return text
    
    for item in cluster:
        longest_character = None
        for character in characters:
            if character.lower() in item.lower() and character.lower() in text.lower() and " "+character.lower()+" " in text.lower():
                
                if longest_character is None or len(character) > len(longest_character):
                    longest_character = character

        if not longest_character is None:            
            result = text.lower().replace(longest_character.lower(), characters[longest_character])

            return match_case(result, text)
    return text


def direct_match(text):
    longest_character = None
    for character in characters:
        if character == text.lower():
            if longest_character is None or len(character) > len(longest_character):
                longest_character = character

    if not longest_character is None:
        replace = re.compile(re.escape(longest_character), re.IGNORECASE)
        text = replace.sub(characters[longest_character], text)
        return text, True

    longest_character = None
    for character in characters:
        if " "+character in text.lower():
            if longest_character is None or len(character) > len(longest_character):
                longest_character = character

    if not longest_character is None:
        replace = re.compile(re.escape(" "+longest_character), re.IGNORECASE)
        text = replace.sub(" " + characters[longest_character], text)
        return text, True


    longest_character = None
    for character in characters:
        if character in text.lower() and character[0] == text[0].lower() and text[0]==text[0].upper():
            if longest_character is None or len(character) > len(longest_character):
                longest_character = character

    if not longest_character is None:
        replace = re.compile(re.escape(longest_character), re.IGNORECASE)
        text = replace.sub(characters[longest_character], text)
        return text, True

    
    return text, False
