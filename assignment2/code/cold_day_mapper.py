#!/usr/bin/env python3
"""mapper.py."""

import sys

# input comes from STDIN (standard input)
data = []
for line in sys.stdin:
    line = line.strip()

    city, date, hi, lo = line.split(',')

    print('{}\t{}\t{}'.format(city, date, lo))
