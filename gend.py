import json
import re

import gender_guesser.detector

gender_guess = gender_guesser.detector.Detector(case_sensitive=False)

with open("genders.json") as genders:
    exceptions = json.load(genders)

def hump_cuts(s):
    yield 0
    for i in range(1, len(s)):
        if s[i-1].islower() and s[i].isupper():
            yield i
    yield len(s)

def humps(s):
    cuts = list(hump_cuts(s))
    for a, b in zip(cuts, cuts[1:]):
        yield s[a:b]

def parts(s):
    for word in re.split(r"\W", s):
        for hump in humps(word):
            yield hump

def guess_gender(name, country=None, split=False):
    if not name:
        return "unknown"
    first_name = name.split()[0].lower()
    guess = exceptions.get(first_name)
    if guess is None:
        guess = gender_guess.get_gender(first_name, country=country)
    if guess == "andy" and country is None:
        guess = guess_gender(name, country="usa")
    if guess.startswith("mostly_"):
        guess = guess[len("mostly_"):]
    if guess == "unknown" and not split:
        guesses = [guess_gender(part, split=True) for part in parts(first_name)]
        for guess in guesses:
            if guess in ['male', 'female']:
                break
    return guess
