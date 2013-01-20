#!/usr/bin/env python
# "rides the fence" to add liquidity to the bitfloor bitcoin financial exchange

#import random
import math, time, os, sys, json, collections
import json_ascii  # TODO: replace with dul.runfun(x,encode)

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'bitfloor', 'lib')))
from bitfloor import RAPI

sys.path.append(os.path.expanduser(os.path.join('~', 'src', 'python-posix-daemon', 'src')))
#from daemon2x import Daemon

from task import SimpleTask, Daemon

class FenceTask(SimpleTask):
    def task(self):
        print('SimpleTask running...')
        time.sleep(1)

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

#if __name__ == "__main__":
#    daemon = FenceTask('/tmp/fence-example.pid')
#    if len(sys.argv) == 2:
#        if 'start' == sys.argv[1]:
#            daemon.start()
#        elif 'stop' == sys.argv[1]:
#            daemon.stop()
#        elif 'restart' == sys.argv[1]:
#            daemon.restart()
#        else:
#            print "Unknown command"
#            sys.exit(2)
#        sys.exit(0)
#    else:
#        print "usage: %s start|stop|restart" % sys.argv[0]
#        sys.exit(2)

if __name__ == "__main__":
    tsk = FenceTask('/tmp/fence.pid')
    tsk.SLEEP_INTERVAL = 1
    tsk.argv(sys.argv)



