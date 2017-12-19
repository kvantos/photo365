#!/usr/bin/env python3

"""
Purpose of this project is to master abstraction thinking for artists.
Generate CSV file for importing to Google Calendar
"""

import random
from calendar import monthrange

YEAR = 2017
header = ["Subject", "Start date", "All Day Event"]

with open('words.txt', "r") as ff:
    words = ff.read()
    words = words.split('\n')


def generate_month(month):
    week, days = monthrange(YEAR, month)
    
    words_selected = set()
    while len(words_selected) < days:
        digit = random.randrange(0, len(words))
        words_selected.add(words[digit])

    day = 1
    message = ",".join(header)
    message += "\n"
    for word in words_selected:
        date = "%02d/%s/%s" % (day, month, YEAR)
        message += "%s,%s,%s\n" % (word, date, "True")
        day += 1
            
    return message


cal = generate_month(12)

with open("photo365_calendar_%i.csv" % YEAR, "w+") as cc:
    cc.write(cal)
    
