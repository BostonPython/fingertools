"""Print a list of attendees for a meetup event."""

# http://www.meetup.com/meetup_api/

import argparse, pprint, urllib, json, random, sys, time
from collections import defaultdict

from keys import API_KEY, GROUP_ID

the_encoding = sys.stdout.encoding or 'utf8'

def meetup(slug, **kwargs):
    kwargs['key'] = API_KEY
    url = "https://api.meetup.com/" + slug
    url += "?" + urllib.urlencode(kwargs)
    print "opening %r" % url
    resp = urllib.urlopen(url)
    j = resp.read()
    #print repr(j).replace(r'\n', '\n')
    j = j.decode('utf-8')
    data = json.loads(j)
    #pprint.pprint(data)
    return data

def list_events(**kwargs):
    """Return a list of events, from the 2/events Meetup API call."""
    kwargs.setdefault('group_id', GROUP_ID)
    events = meetup("2/events", **kwargs)['results']
    for event in events:
        event['when'] = time.strftime("%d %b %Y", time.localtime(event['time']//1000))
    return events

def event_answers(event_id):
    """Return a dict mapping {"yes","no","maybe"} onto (username, num_guests) pairs."""
    answers = defaultdict(list)
    rsvps = meetup("2/rsvps", event_id=event_id)
    for rsvp in rsvps['results']:
        answers[rsvp['response']].append((rsvp['member']['name'], rsvp['guests']))
    return answers

def event_attendees(event_id):
    """Return the set of attendees in the yes or waiting list."""
    rsvps = meetup("2/rsvps", event_id=event_id)
    attendees = set()
    for rsvp in rsvps['results']:
        if rsvp['response'] in ['yes', 'waitlist']:
            member = rsvp['member']
            attendees.add((member['member_id'], member['name']))
    return attendees

def show_attendees(event_id):
    answers = event_answers(event_id)
    for ans in answers.keys():
        members = sorted(answers[ans])
        count = len(members) + sum(g for n,g in members)
        print "== %d %s:" % (count, ans)
        for m, g in members:
            x = "   "+m+(" +%d"%g if g else "")
            try:
                print x
            except:
                print repr(x)

def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--global')
    subparsers = parser.add_subparsers(dest="command")

    events_parser = subparsers.add_parser('events')
    events_parser.add_argument('--csv', action='store_true')

    attendees_parser = subparsers.add_parser('attendees')
    attendees_parser.add_argument("event_id", type=int, nargs='?')

    tutorials_parser = subparsers.add_parser('overlap')

    return parser

def yes(event_id):
    """Return a list of names of people who RSVP'd yes to an event."""
    answers = event_answers(event_id)
    yesses = [a[0].title() for a in answers['yes']]
    return sorted(yesses)

def main(argv):
    parser = create_arg_parser()
    args = parser.parse_args(argv)

    if args.command == "attendees":
        if args.event_id is None:
            events = list_events(status="upcoming")
            for event in events:
                print "\n\n#%(id)s: %(when)s %(name)s, %(yes_rsvp_count)d" % event
                show_attendees(event['id'])
        else:
            show_attendees(args.event_id)
    elif args.command == "events":
        events = list_events(status="upcoming,past")
        if args.csv:
            import csv
            with open("events.csv", "wb") as fcsv:
                writer = csv.writer(fcsv)
                events = list_events(status="past")
                for event in events:
                    writer.writerow((
                        event['when'],
                        event['name'],
                        event['event_url'],
                        event['yes_rsvp_count'],
                    ))
        else:
            for event in events:
                print "#%(id)s: %(when)s %(name)s, %(yes_rsvp_count)d" % event
    elif args.command == "overlap":
        events = {
            "76032852": "PyCon 1",
            "76034482": "PyCon 2",
            #"100277162": "Intro Python",
            #"100333402": "Bayesian",
            #"100330612": "Open Source",
            #"100333602": "Intermediate Twisted",
        }
        attending = defaultdict(list)
        for event_id in events:
            for attendee in event_attendees(event_id):
                attending[attendee].append(event_id)
        overlaps = (
            (attendee[1], [events[e] for e in eventlist])
            for attendee, eventlist in attending.items()
            if len(eventlist) > 1
            )
        for i, (who, what) in enumerate(overlaps, 1):
            print "%3d  %s: %s" % (i, who.encode(the_encoding), what)

if __name__ == '__main__':
    main(sys.argv[1:])
