#!/usr/bin/env python3
"""
Module Docstring
"""

import json
import string
from pprint import pprint
from omegaconf import OmegaConf

# Load the config files

# Load the word files
f = open("words.json")
word_lists = json.load(f)

vwords = word_lists['valid_words']
pwords = word_lists['past_words']


def scoreletters(wdict):
    """Builds a dictionary of letter scores based on the number of times each letter appears in each position in the remaining words"""
    scoreDict = {}
    # Make a list of the alphabet
    alphabetlist = list(string.ascii_lowercase)
    # Build the skeleton of our score dictionary
    for l in alphabetlist:
        scoreDict[l] = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
    # Iterate through our word list to score the number of times letters appear in each position
    for w in wdict:
        i = 0
        for letter in wdict[w]['letterList']:
            scoreDict[letter][i] += 1
            i += 1

    return scoreDict


def scorewords(wdict, lscores):
    scoreDict = {}
    for w in wdict:
        i = 0
        score = 0
        for l in wdict[w]['letterList']:
            score += lscores[l][i]
            i += 1
        scoreDict[w] = score

    return scoreDict


def main():
    global wordScores
    global awords
    # Build list of available words
    awords = {}
    for w in vwords:
        if w not in pwords:
            awords[w] = {
                "letterList": list(w),
                "score": 0
            }

    letterScores = scoreletters(awords)
    wordScores = scorewords(awords, letterScores)

    # Update word dictionary with scores
    for w in awords:
        awords[w]['score'] = wordScores[w]

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()