"""Show all the members of a group"""

# http://www.meetup.com/meetup_api/

import pprint, time
from collections import defaultdict

import meetup

meetup.DEBUG = 0

def group_members(**kwargs):
    """Return a list of the members of a group."""
    members = meetup.meetup("members", **kwargs)
    for m in members:
        last_visit = time.strptime(m['visited'][:-4], "%Y-%m-%d %H:%M:%S")
        m['visitage'] = time.time() - time.mktime(last_visit)
        joined = time.strptime(m['joined'].replace("EDT ", "").replace("EST ", ""), "%a %b %d %H:%M:%S %Y")
        m['joinage'] = time.time() - time.mktime(joined)
    return members

def print_members(members):
    members = sorted(members, key=lambda m: int(m['id']))
    for member in members:
        try:
            name = member['name'].encode('ascii')
        except:
            name = repr(member['name'])
        print "#%s: %s, %s" % (member['id'], name, member['joined'])
    print "%d members" % len(members)

def show_other_group(name, us, other=None):
    other = other or group_members(group_urlname=name)
    both = set(m['id'] for m in other) & set(m['id'] for m in us)
    u, o, b = len(us), len(other), len(both)
    percent_us = 100.0*b/u if u else 0.0
    percent_other = 100.0*b/o if o else 0.0
    #print "%-15s %4d members, %s %s (%4d overlap, %2d%% of us, %2d%% of them)" % (name[:15], o, active_summary(other, 3), active_summary(other, 6), b, percent_us, percent_other)
    return "%4d %2d%%/%2d%%" % (b, percent_us, percent_other)

def active_count(members, secs):
    return sum(1 if m['visitage'] < secs else 0 for m in members)

def active_summary(members, mos):
    if members:
        count = active_count(members, mos*30*24*60*60)
        return "%3d%% <%dmo" % (100.0*count/len(members), mos)
    else:
        return " --  <%dmo" % (mos,)

def join_count(members, sec_lo, sec_hi):
    return sum(1 if sec_lo <= m['joinage'] < sec_hi else 0 for m in members)

def show_group(name, members, baseline=None):
    if baseline is None:
        sign = '='
        delta = 0
    else:
        delta = len(members) - baseline
        if delta < 0:
            sign = '-'
            delta = abs(delta)
        else:
            sign = '+'

    # 99.4 here so that if it's really 100%, it will still fit in 2 chars.
    joining = "  ".join("%s:%2d%%" % (m, (99.4*c/len(members)) if members else 0) for m,c in join_buckets(members))
    other_group_share = show_other_group(name, bospy, members) if bospy != members else "     --     "

    print "%-25s %5d (%s%4d)  %s %s   %s   [%s]" % (
        name[:25], len(members), sign, delta,
        active_summary(members, 3), active_summary(members, 6),
        joining, other_group_share,
    )

def join_buckets(members):
    mo_buckets = [0, 1, 2, 3, 4, 6, ]
    for i in range(len(mo_buckets)-1):
        sec_lo = mo_buckets[i] * 30*24*60*60
        sec_hi = mo_buckets[i+1] * 30*24*60*60
        yield mo_buckets[i+1], join_count(members, sec_lo, sec_hi)

bospy = group_members(group_urlname='bostonpython')
#print_members(bospy)
print(
"-- group --------------   -size--delta-   ----- active -----   - joined ------------------------   -- overlap ---"
#bostonpython               5897 (=   0)   22% <3mo  33% <6mo   1: 2%  2: 0%  3: 1%  4: 1%  6: 3%   [     --     ]
)

show_group('bostonpython', bospy)

OTHERS = """
    PyLadies-Boston
    PyData-Boston
    nycpython
    NYC-PyLadies
    djangoboston
    bostonphp
    Boston_New_Technology
    sfpython
    django-nyc
    frpythoneers
    pdxpython
    Openstack-Boston
    boston-java
    TechinmotionBoston
    bostonsoftware
    Open-edX-Boston
    openedX
"""
#    Code-Mentors-Boston
#    Rails-Boston
#    Automated-Testing-Boston
#    javascript-2
#    Boston-Predictive-Analytics
#    Lean-Startup-Circle-Boston
#    Boston-MongoDB-User-Group
#    austinpython
#    dcpython
#    The-Greater-Hartford-Python-Group
#    Boston-Twisted-Python
#    phillypug
#    python-atlanta
#    jQuery-Boston
#    bostonappengine
#    mysqlbos
#    CustomMade-Hackathon
#    Boston-Startup-Weekend
#    Rails-Boston
#    newtech-73
#    OpenCoffee-Cambridge-Meetup
#    Boston-Mobile-App-Developers-iPhone-Droid-iPad
#    The-Cambridge-Semantic-Web-Meetup-Group

for other in OTHERS.split():
    members = group_members(group_urlname=other)
    show_group(other, members, len(bospy))
