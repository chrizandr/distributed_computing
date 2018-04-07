#!/usr/bin/env python3
"""reducer.py."""

import sys

current_word = None
total_num = 0
current_count = float('inf')
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = float(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    if float(count) < current_count:
        current_count = count
        current_word = word

print("{}\t{}".format(current_word, current_count))
