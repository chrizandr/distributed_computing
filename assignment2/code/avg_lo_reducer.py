#!/usr/bin/env python
"""reducer.py."""

import sys

current_word = []
total_num = 0
current_count = -1*float('inf')
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    word, count, num = line.split('\t', 2)

    # convert count (currently a string) to int
    try:
        count = float(count) * int(num)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count.append(count)
        total_num += int(num)
    else:
        if current_word:
            # write result to STDOUT
            print '%s\t%s\t%s' % (current_word, sum(current_count)/total_num, total_num)
        current_count = [count]
        total_num = int(num)
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s\t%s' % (current_word, sum(current_count)/total_num, total_num)
