#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""How many pizzas do we need?"""

import math

people = int(input("How many RSVPs? ") or 0)

# The MUC (Meetup Universal Constant)
muc = 65
muc_str = input(f"What percentage will show up? [{muc}] ")
if muc_str.strip():
    muc = int(muc_str.strip())


attending = int(people * muc / 100)

print()
print(f"👪  {attending} people will show up (guess)\n")

# Appetite estimation
slices = attending * 2.5

# Basic pizza geometry
pies = slices / 8

print(f"🍕  {pies:.2f} pizzas (or so)")

# From answers to the 10/2012 project night:
#   81 answers
#   26 meat 32%
#   37 veg 45%
#   16 cheese 20%
#   2 vegan 3%

# Answers to the 4/2013 presentation night:
#   163 answers (if someone said "meat or cheese", I counted it as two votes: one for meat, one for cheese).
#   33 cheese 20%
#   63 meat 39%
#   67 veggie 41%

meat = int(.39 * pies) or 1
veggie = int(.41 * pies) or 1
cheese = pies - meat - veggie
if cheese < 1:
    cheese = 1
cheese = int(math.ceil(cheese))

print()
print(f"🧀  {cheese} cheese")
print(f"🍖  {meat} meat")
print(f"🍅  {veggie} veggie")
print()
print(f"🍕  {(cheese+meat+veggie)} total")

# Soda!

# Answers to the 10/2014 project night:
#   53 water        55%
#   21 Coke         20%
#   14 Diet Coke    15%
#    8 Sprite       10%

cups = 2 * attending
cups_per_bottle = 67.0 / 8  # 67 ounces in a 2-liter bottle

def round_bottle(b):
    if b - int(b) < .25:
        b = int(b)
    else:
        b = int(b+1)
    return b or 1

cokes = round_bottle(.20 * cups / cups_per_bottle)
diet_cokes = round_bottle(.15 * cups / cups_per_bottle)
sprites = round_bottle(.10 * cups / cups_per_bottle)

print()
print(f"   {cokes} cokes (2 liter)")
print(f"   {diet_cokes} diet cokes (2 liter)")
print(f"   {sprites} sprites (2 liter)")
