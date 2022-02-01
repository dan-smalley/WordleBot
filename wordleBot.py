import json
from omegaconf import OmegaConf

# Load the config files

# Load the word files
f = open("words.json")
word_lists = json.load(f)

vwords = word_lists['valid_words']
pwords = word_lists['past_words']

# Build list of available words
awords = []
for w in vwords:
    if w not in pwords:
        awords.append(w)
        