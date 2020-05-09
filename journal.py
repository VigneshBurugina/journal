import time
import datetime


class journal:
    '''Journal Class
    
    Used for logging events and measuring runtime

    Methods:

    start()
    show()
    save()
    end()
    log()
    measure()
    
    '''

    def __init__(self, name, file='journal.log', autosave=True,autostart=True):
        '''Constructor for journal class
        
        Attributes:
        self.name - Name of the journal
        self.file - Log File (default: journal.log)
        self.autosave - Autosave state for logs
        self.journal_handle - File handle of log file
        self.autostart - Autostarts log file (using self.start method and overwrites)
        '''
        self.name = name
        self.file = file
        self.autosave = autosave
        self.journal_handle = ''
        self.autostart = autostart
        if self.autostart:
            self.start(overwrite=True)

    def _cur_time(self,strg=True):
        '''Returns current system time
        using datetme module 
        (for string set strg as True)'''
        if strg:
            return str(datetime.datetime.now())
        return datetime.datetime.now()

    def start(self, overwrite=False, ts=True):
        '''Starts the journal file and sets the journal object file handle
        Usage: journal object.start([overwrite],[ts])
        Set ts as True to create a timestamp
        Set overwrite as True to overwrite if log file exists 
        '''
        try:
            _temp = open(self.file, 'r')
            del _temp
            if overwrite:
                self.journal_handle = open(self.file, 'w')
                if ts == True:
                    self.log(
                        f'Created on:{self._cur_time()}',ts=False)
                self.log(f'{"-"*10}{self.name} Log{"-"*10}',ts=False)
            else:
                print('Journal alredy exists (Use overwrite arg to replace)')
        except FileNotFoundError:
            self.journal_handle = open(self.file, 'w')
            if ts == True:
                self.log(
                f'Created on:{self._cur_time()}',ts=False)
            self.log(f'{"-"*10}{self.name}{"-"*10}',ts=False)
        return None

    def save(self):
        '''Flushes the buffer to the file storage'''
        if self.journal_handle == '':
            print('Journal has not been started')
            return None
        self.journal_handle.flush()
        return None

    def end(self):
        '''Closes the log file'''
        self.journal_handle.close()
        self.journal_handle = ''
        return None
    
    def show(self):
        '''Saves and prints out the current log file's contents
    
        USAGE:
        [journal object].show()
        '''
        self.save()
        data = self.journal_handle.readlines()
        for i in data:
            print(i.rstrip('\n'))

    def log(self, event, ts=True):
        '''Use to log events

        Usage:
        [journal object].log(event_to_log,[ts])
        or
        @[journal object].log
        Set ts to True to timestamp
        Using decorator logs the function call and call's arguments
        '''
        def func_wrapper(*a):
            self.log(
                f'Called Function: {event.__name__} with Arguments {tuple(a)}')
            return event(*a)

        if self.journal_handle == "":
            print('Journal has not been started')
            return None
        if callable(event):
            return func_wrapper
        else:
            if ts:
                ts = self._cur_time() + ':'
            else:
                ts = ''
            self.journal_handle.write(f'{ts}{event}')
            self.journal_handle.write('\n')
            if self.autosave:
                self.journal_handle.flush()
            del event
            return None

    def measure(self, func, args=False, log=False):
        '''Use to measure time taken for function to execute

        Usage:
        @[journal object].measure
        Set args to True to display arguments passed 
        Set log to True to log the funtion call
        '''
        start_time = 0
        end_time = 0

        def wrapper(*a):
            nonlocal start_time
            nonlocal end_time
            if args:
                print(f'{func.__name__} arguments: {a}')
            start_time = self._cur_time(strg=False)
            print(f'Started: {func.__name__} at {start_time}')
            res = func(*a)
            end_time = self._cur_time(strg=False)
            print(f'Finished: {func.__name__} at {end_time}')
            print(f'Time Taken: {end_time-start_time}')
            return res
        if log and self.journal_handle != '':
            self.log(
                f'Measured {func.__name__} runtime: {end_time-start_time}')
        elif self.journal_handle == '':
            print('Journal has not been started')
        return wrapper

