#!/usr/bin/env python

"""Checks which words from a list are valid and available Twitter usernames."""

from time import sleep
from json import loads
from httplib import HTTPConnection, BadStatusLine
from socket import error as socket_error
from sys import stderr

# Edit the next list as you like
words = ['a', 'list', 'of', 'possible', 'unused', 'twitter', 'usernames']

conn = HTTPConnection("twitter.com", 80, timeout=10)
path = "/users/username_available?suggest=1&username="
for word in words:
    sleep(1)
    try:
        conn.request('GET', '%s%s' % (path, word))
    except socket_error, e:
        print >> stderr, 'Could not retrieve: %s' % word
        continue
    try:
        response = conn.getresponse()
    except BadStatusLine, e:
        print >> stderr, 'Bad status line: %s' % word
        sleep(60)
        conn = HTTPConnection("twitter.com", 80, timeout=10)
        continue
    data = response.read()
    try:
        data = loads(data)
    except ValueError:
        print >> stderr, 'Could not parse JSON: %s' % word
        continue        
    print '%s available? %s' % (word, data["valid"])
    if data["valid"]:
        print >> stderr, word