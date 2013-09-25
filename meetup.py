"""Rough and ready meetup.com api wrapper."""

import json
import urllib

from keys import API_KEY

DEBUG = 1

def meetup_call(slug, **kwargs):
    kwargs['key'] = API_KEY
    url = "https://api.meetup.com/" + slug
    url += "?" + urllib.urlencode(kwargs)
    return meetup_url_call(url)

def meetup_url_call(url):
    if DEBUG > 0:
        print "opening %r" % url
    resp = urllib.urlopen(url)
    j = resp.read().decode('iso8859-1')
    return json.loads(j)

def meetup(slug, **kwargs):
    results = []
    response = meetup_call(slug, **kwargs)

    while True:
        try:
            next = response['meta']['next']
        except KeyError:
            print response
            raise
        results.extend(response['results'])

        if not next:
            break

        response = meetup_url_call(next)

    return results
