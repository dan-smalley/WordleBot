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

valid_words = word_lists['valid_words']
past_words = word_lists['past_words']
override_starting_word = 'adieu'
solution_index = -32


def score_letters(word_dict):
    """Builds a dictionary of letter scores based on the number of times
    each letter appears in each position in the remaining words"""
    score_dict = {}
    # Make a list of the alphabet
    alphabet_list = list(string.ascii_lowercase)
    # Build the skeleton of our score dictionary
    for letter in alphabet_list:
        score_dict[letter] = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
    # Iterate through our word list to score the number of times letters appear in each position
    for word in word_dict:
        for i, letter in enumerate(word_dict[word]['letter_list']):
            score_dict[letter][i] += 1

    return score_dict


def score_words(word_dict, letter_scores, banned_letters):
    score_dict = {}
    for word in word_dict:
        score = 0
        score_list = []
        for i, letter in enumerate(word_dict[word]['letter_list']):
            if letter not in banned_letters:
                score += letter_scores[letter][i]
                score_list.append(letter_scores[letter][i])
        score_dict[word] = {'score_list': score_list, 'total_score': score}

    return score_dict


def highest_score(word_dict):
    words = []
    scores = []
    for word in word_dict:
        words.append(word)
        scores.append(word_dict[word]['total_score'])

    return words[scores.index(max(scores))], words[scores.index(min(scores))]


def purge_words(word_dict, guess, result):
    """Builds a list of words to purge for the available word set"""
    purge_list = []
    # Turn current guess into a list
    guess_list = list(guess)

    # Iterate through each letter and purge words based on the result
    for i, letter in enumerate(guess_list):
        # Purge words containing an invalid letter
        if result[i] == 0:
            for word in word_dict:
                if letter in word:
                    purge_list.append(word)
        # Purge words with letters in incorrect position
        elif result[i] == 2:
            for word in word_dict:
                if word_dict[word]['letter_list'][i] != letter:
                    purge_list.append(word)
        # Purge words that do not contain a correct letter
        elif result[i] == 1:
            for word in word_dict:
                if letter not in word:
                    purge_list.append(word)

    return purge_list


def play_word(word):
    """Simulates playing rounds of wordle using the last word in the past words list"""
    # Get current word as a list of letters
    current_word = list(past_words[solution_index])
    # Convert guessed word to a list of letters
    played_word = list(word)

    result = []
    # Iterate through matches
    for i, letter in enumerate(played_word):
        if letter == current_word[i]:
            result.append(2)
        elif letter in current_word:
            result.append(1)
        else:
            result.append(0)

    return result


def main():
    global word_scores
    global available_words
    # Build main our word dictionary
    available_words = {}
    for word in valid_words:
        if word not in past_words:
            available_words[word] = {
                'letter_list': list(word),
                'score_list': [],
                'total_score': None
            }
    # Add last word for dev purposes
    available_words[past_words[solution_index]] = {
                'letter_list': list(past_words[solution_index]),
                'score_list': [],
                'total_score': None
            }

    # Start playing guesses
    result = []
    banned_letters = []
    i = 1
    while sum(result) < 10:
        # Get letter scores and initial word scores
        letter_scores = score_letters(available_words)
        word_scores = score_words(available_words, letter_scores, banned_letters)

        # Update word dictionary with scores
        for word in available_words:
            available_words[word]['score_list'] = word_scores[word]['score_list']
            available_words[word]['total_score'] = word_scores[word]['total_score']
        # Get highest scoring word
        best_word, worst_word = highest_score(available_words)
        # Override starting word
        if i == 1 and override_starting_word is not None:
            best_word = override_starting_word
        # print('Best:', best_word, available_words[best_word]['total_score'])
        # print('Worst:', worst_word, available_words[worst_word]['total_score'])
        print(f'{best_word} {available_words[best_word]["total_score"]}  //  '
              f'{worst_word} {available_words[worst_word]["total_score"]} //  {len(available_words)}')

        # Play highest scoring word
        result = play_word(best_word)
        if sum(result) < 10:
            print(f'Guess {i}: {best_word}   ---  {result}')
            # Purge words that are eliminated by result
            purge_list = purge_words(available_words,best_word,result)
            for word in purge_list:
                if word in available_words:
                    del available_words[word]
            if best_word in available_words:
                del available_words[best_word]
            # Add banned letters to exclude from scoring
            for idx, item in enumerate(result):
                if item == 0 and best_word[idx] not in banned_letters:
                    banned_letters.append(best_word[idx])
            # print(f'{len(available_words)} possible words left')
            i += 1
    print(f'Solution {best_word} found in {i} guesses')


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
