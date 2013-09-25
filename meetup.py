"""Rough and ready meetup.com api wrapper."""

import json
import urllib

from keys import API_KEY

DEBUG = 1

def meetup_call(slug, **kwargs):
    kwargs['key'] = API_KEY
    url = "https://api.meetup.com/" + slug
    url += "?" + urllib.urlencode(kwargs)
    if DEBUG > 0:
        print "opening %r" % url
    resp = urllib.urlopen(url)
    j = resp.read().decode('iso8859-1')
    return json.loads(j)

def meetup(slug, **kwargs):
    results = []
    offset = 0
    while True:
        moreresults = meetup_call(slug, offset=offset, **kwargs)
        try:
            meta = moreresults['meta']
        except KeyError:
            print moreresults
            raise
        #print "Count = %d, total count = %d" % (meta['count'], meta['total_count'])
        if meta['count'] == 0:
            break
        results.extend(moreresults['results'])
        offset += 1
    return results
