"""How many pizzas do we need?"""

import math

people = int(raw_input("How many RSVPs? "))

# The MUC (Meetup Universal Constant)
muc = 65
muc_str = raw_input("What percentage will show up? [%d] " % muc)
if muc_str.strip():
    muc = int(muc_str.strip())

attending = people * muc / 100

print
print "%d people will show up (guess)" % attending

# Appetite estimation
slices = attending * 2.5

# Basic pizza geometry
pies = slices / 8

print "%.1f pizzas (or so)" % pies

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

print
print "%2d cheese" % cheese
print "%2d meat" % meat
print "%2d veggie" % veggie
print
print "%2d total" % (cheese + meat + veggie)

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

print
print "%2d cokes (%d 20-oz)" % (cokes, round_bottle(.20 * attending))
print "%2d diet cokes (%d 20-oz)" % (diet_cokes, round_bottle(.15 * attending))
print "%2d sprites (%d 20-oz)" % (sprites, round_bottle(.10 * attending))
