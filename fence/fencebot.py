#!/usr/bin/env python
# "rides the fence" to add liquidity to the bitfloor bitcoin financial exchange

#import random
import math, time, os, sys, json, collections
import json_ascii  # TODO: replace with dul.runfun(x,encode)

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'bitfloor', 'lib')))
from bitfloor import RAPI

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'python-posix-daemon', 'src')))

DEFAULT_KEY_PATH = os.path.join('/etc','security','bfl.json')

from task import RepeatedTask

class FenceTask(RepeatedTask):
    def __init__(self, key_path=DEFAULT_KEY_PATH):
        super(FenceTask, self).__init__()
        with open(key_path) as f:
            config = json.load(f, object_hook=json_ascii.decode_dict)
            self.bf = RAPI(product_id=1, key=config['key'], secret=config['secret'])

    def task(self):
        print('FenceTask running...')
        try:
            err = False
            last = float(bf.ticker()['price'])
            book = floatify(bf.book(2))
            brink = floatify(bf.book(1))
            mean_book = mean(book)
            print mean_book, last, brink
        except:
            err = True
        print '-' * 60
        time.sleep(3.723)


if __name__ == "__main__":
    tsk = FenceTask()
    tsk.SLEEP_INTERVAL = 3
    tsk.argv(sys.argv)



