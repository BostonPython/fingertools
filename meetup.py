"""Rough and ready meetup.com api wrapper."""

import json
import re
import urllib, urllib2

from keys import API_KEY

DEBUG = 1
SECRET = 1

def meetup_call(slug, **kwargs):
    kwargs['key'] = API_KEY
    url = "https://api.meetup.com/" + slug
    url += "?" + urllib.urlencode(kwargs)
    return meetup_url_call(url)

def meetup_url_call(url):
    if DEBUG > 0:
        show_url = url
        if SECRET:
            show_url = re.sub(r"key=[0-9a-fA-F]{30}", "key=xyzzy", show_url)
        print "opening %r" % show_url

    headers = { 'Accept-Charset': 'utf-8' }
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    j = resp.read()
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
