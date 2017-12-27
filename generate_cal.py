#!/usr/bin/env python3

"""
Purpose of this project is to master abstraction thinking for artists.
Generate CSV file for importing to Google Calendar
"""

import random
from calendar import monthrange, isleap
import pickle

YEAR = 2018

if isleap(YEAR):
    num_days = 366
else:
    num_days = 365

header = ["Subject", "Start date", "All Day Event", "Description"]

with open('dict_data.bin', "rb") as ff:
    words = pickle.load(ff)

words_list = list(words)
random.shuffle(words_list)
words_selected = words_list[:num_days]


def generate_month(month):
    week, days = monthrange(YEAR, month)
    global words_selected

    day = 1
    message = ""
    while day <= days:
        word = words_selected.pop(-1)
        definition = words[word]
        definition = definition.strip('\'')
        definition = definition.replace("\"", "\'")
        date = "%02d/%s/%s" % (day, month, YEAR)
        message += "%s,%s,%s,\"%s\"\n" % (word.upper(), date, "True", definition)
        day += 1

    return message


cal = ",".join(header)
cal += "\n"
# cal += generate_month(12)
for month in range(1, 13):
    print("Generate %i month" % month)
    cal += generate_month(month)

with open("photo365_calendar_%i.csv" % YEAR, "w+") as cc:
    cc.write(cal)
    
