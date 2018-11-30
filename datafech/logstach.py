import logging
import logstash
import sys
host = '192.168.3.116'
logger = logging.getLogger('python-logstash-logger')
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(message)s")    # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)
logger.addHandler(logstash.TCPLogstashHandler(host, 9600, version=1))

def info(message):
    return logger.info(message)

def error(message):
    return logger.error(message)

