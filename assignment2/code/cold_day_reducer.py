#!/usr/bin/env python
"""reducer.py."""

import sys

current_word = None
current_date = None
current_count = float('inf')
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, date, count = line.split('\t', 2)

    # convert count (currently a string) to int
    try:
        count = float(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        if count < current_count:
            current_count = count
            cuurent_date = date
    else:
        if current_word:
            # write result to STDOUT
            print '%s\t%s\t%s' % (current_word, current_date, current_count)
        current_count = count
        current_date = date
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s\t%s' % (current_word, current_date, current_count)
