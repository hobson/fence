import sys, os, time, atexit
from signal import SIGTERM

class SimpleTask:
    """
    Generic background process (daemon, task).
    Usage: subclass the SimpleTaks class and do your task in the run() method
    """
    SLEEP_INTERVAL = 1.1  # seconds between loops of the run task
    LOG_FILE = '/etc/log/simpletask.log'
    DEBUG = True
    
    def __init__(self, pidfile='/tmp/SimpleTask', stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, logfile=LOG_FILE):
        if self.DEBUG:
            print 'initializing SimpleTask object'
        #self.flog = open(LOGFILE)
        self.task_counter = 0
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
    
    def daemonize(self):
        """
        UNIX double-fork magic, from Stevens' "Advanced Programming in the UNIX Environment"
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        if self.DEBUG:
            print 'daemonizing SimpleTask object'
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        if self.DEBUG:
            print 'daemonizing successful'
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
    
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        if self.DEBUG:
            print 'daemonizing #2 successful'
    
        # redirect standard file descriptors
        sys.stdout.flush()
        if self.DEBUG:
            print 'flushed stdout'
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        if self.DEBUG:
            print 'opened stdin, stdout, stderr'
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        if self.DEBUG:
            print 'writing pid file....'
        # write pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        if self.DEBUG:
            print 'finished daemonizing'
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start the task
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. SimpleTask already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the task
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if not pid:
            message = "pidfile %s does not exist. Task not running?\n"
            sys.stderr.write(message % self.pidfile)
            return # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stderr.write(str(err))
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def argv(self, argv):
        if argv is None:
            argv = argv
        if len(argv) == 2:
            if 'start' == argv[1]:
                self.start()
            elif 'stop' == argv[1]:
                self.stop()
            elif 'restart' == argv[1]:
                self.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % argv[0]
            sys.exit(2)

    def task(self):
         sys.stderr.write('You should probably override this function to do something useful that chips away at the total entropy in the universe.')

    def run(self):
        """
        Override this method (and/or the `task` method above with useful stuff.
        `run` will be called after the process has been
        pushed to the backgrounded by start() or restart().  If you just want
        a task to be repeatedly run with a SLEEP_INTERVAL sleep time between
        calls, just leave this method as-is and override the `task` method.
        """
        while True:
            self.task()
            self.task_counter += 1
            sleep(SLEEP_INTERVAL)

