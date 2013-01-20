#!/usr/bin/env python
# "rides the fence" to add liquidity to the bitfloor bitcoin financial exchange

#import random
import math, time, os, sys, json, collections
import json_ascii  # TODO: replace with dul.runfun(x,encode)

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'bitfloor', 'lib')))
from bitfloor import RAPI

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'python-posix-daemon', 'src')))
from daemon2x import Daemon

class FenceDaemon(Daemon):
    def run(self):
        while True:
            time.sleep(SLEEP_INTERVAL)

def main():
    path = os.path.join('/etc','security','bfl.json')

    with open(path) as f:
        config = json.load(f, object_hook=json_ascii.decode_dict)
    print config
    bf = RAPI(product_id=1, key=config['key'], secret=config['secret'])

    olatency = [] # order latency
    clatency = [] # cancel latency

    orders = []
    while True:
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
    task = task.SimpleTask('/tmp/fence.pid')
    task.SLEEP_INTERVAL = 4.0
    def printer(self):
        print('SimpleTask running...')
    task.task = printer
    task.argv(sys.argv)



