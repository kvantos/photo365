#!/usr/bin/env python3

"""
Synchronize local dict with dict.org
"""

import time
import pickle
from dictdclient import Connection, Database
import threading
import queue

data_file = "dict_data.bin"

with open('words.txt', "r") as ff:
    words = ff.read()
    words = words.split('\n')
    words.remove('')

words_def = {}


def word_getter():
    global words_def

    while True:
        con = Connection("dict.org")
        db = Database(con, "wn")
#        db = Database(con, "fd-eng-rus")
        word = q.get()
        if word is None:
            break

        print("Getting %s" % word)
        try:
            res_list = db.define(word)
            if len(res_list):
                words_def[word] = res_list[0].defstr
        except Exception:
            pass
        
        q.task_done()
        time.sleep(1)


q = queue.Queue()
threads = []
tr_num = 8

for i in range(tr_num):
    t = threading.Thread(target=word_getter)
    t.start()
    threads.append(t)

for word in words:
    q.put(word)

# block until all tasks are done
q.join()
    
# stop workers
for i in range(tr_num):
    q.put(None)
    
for t in threads:
    t.join()

    
with open(data_file, 'wb') as fp:
    pickle.dump(words_def, fp)

print("Number of words total: %i" % len(words))
print("Number of get words: %i" % len(list(words_def)))
