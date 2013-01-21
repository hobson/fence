import sys, os, time, atexit
from signal import SIGTERM

class RepeatedTask(object):
    """
    Generic background process (daemon, task).
    Usage: subclass the RepeatedTask class and do your task in the run() method
    """
    WARN_LEVEL = 2
    
    def __init__(self, pidfile='/tmp/RepeatedTask', stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, logfile=None, debug=True, verbose=True):
        self.SLEEP_INTERVAL = 3  # seconds between calls of the task() method
        self.LOG_FILE = logfile or '/etc/log/repeated_task.log'
        self.DEBUG = debug
        self.VERBOSE = verbose
        self.MESSAGES = ('INFO', 'DEBUG', 'WARNING', 'ERROR', 'FATAL')
        self.RAISE_LEVEL = self.MESSAGES.index('FATAL')

        #self.flog = open(LOGFILE)
        self.task_counter = 0
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def message(self, msg, level=1):
        if isinstance(level, basestring) and len(level.strip()):
            try:
                level = (l for l, prefix in enumerate(self.MESSAGES) if prefix.lower()[0] == level.strip()[0].lower()).next()
            except StopIteration:
                level = 2
        prefix = self.MESSAGES[min(max(level, 0), len(self.MESSAGES))]
        if level > 0:
            if level >= self.RAISE_LEVEL:
                raise(RuntimeError, str(prefix + ': ' + str(msg)))
            elif self.DEBUG or level >= self.WARN_LEVEL or self.VERBOSE:
                sys.stderr.write(prefix + ': ' + str(msg) + '\n')
        elif self.VERBOSE:
            print(prefix + ': ' + str(msg) + '\n')

    def daemonize(self):
        """
        UNIX double-fork magic, from Stevens' "Advanced Programming in the UNIX Environment"
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        self.message('daemonizing RepeatedTask object', 'DEBUG')
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
        self.message('daemonizing successful', 'DEBUG')
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
            # don't raise an exception, just write the message and exit(1)
            self.message("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror), 'ERROR')
            sys.exit(1)
        self.message('Second fork was successful.', 'DEBUG')

        # redirect standard file descriptors
        sys.stdout.flush()
        if self.DEBUG:
            print 'flushed stdout'
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        self.message('Opened stdin, stdout, stderr, now redirecting them...', 'DEBUG')
        # duplicates si to sys.stdin, closing stdin first, if necessary
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        self.message('writing pid file....', 'DEBUG')
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile,'w+').write("%s\n" % pid)
        self.message('Finished daemonizing RepeatedTask', 'DEBUG')
    
    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """
        Start parent (conductor) task to call task() at the specified interval
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
    
        if pid:
            message = "pidfile %s already exist. RepeatedTask already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        
        # Start the task
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the parent (conductor) task
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
            time.sleep(self.SLEEP_INTERVAL)

