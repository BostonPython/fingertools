"""Guess at genders"""

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

TITLES = {
    'ms.': 'female',
    'mrs.': 'female',
    'mr.': 'male',
}

def first_name(name):
    """First name, but use next if first is an initial or title."""
    words = name.split()
    first = words[0]
    if len(words) > 2 and first.lower() not in TITLES:
        if first.endswith('.') and len(first) <= 4:
            first = words[1]
        if len(first) == 1:
            first = words[1]
        if first == 'Dr':
            first = words[1]
    return first

GOOD_GUESSES = ['male', 'female']

def guess_gender(name, country=None, split=False):
    if not name:
        return "unknown"

    # A parenthetical anywhere is the best indicator.
    paren = re.search(r"\((\w+)\)", name)
    if paren:
        guess = guess_gender(paren.group(1))
        if guess in GOOD_GUESSES:
            return guess

    first = first_name(name)
    first_lower = first.lower()
    guess = TITLES.get(first_lower)
    if guess is None:
        guess = exceptions.get(first_lower)
    if guess is None:
        guess = gender_guess.get_gender(first, country=country)
    if guess == "andy" and country is None:
        guess = guess_gender(name, country="usa", split=split)
    if guess.startswith("mostly_"):
        guess = guess[len("mostly_"):]
    if guess not in GOOD_GUESSES and not split:
        guesses = [guess_gender(part, split=True) for part in parts(first)]
        for guess in guesses:
            if guess in GOOD_GUESSES:
                break
    return guess
