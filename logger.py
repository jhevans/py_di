__author__ = 'JohnH.Evans'


class PrintLogger(object):
    def log(self, message):
        print message


class FileLogger(object):
    def log(self, message):
        with open(r'C:\temp\foo_log.txt', 'a') as f:
            f.write(message)