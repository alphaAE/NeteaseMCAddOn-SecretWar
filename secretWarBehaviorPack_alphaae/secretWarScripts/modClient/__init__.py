import logging
import sys


def makeLogger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)7s][SecretWarClient] %(message)s'))
    log = logging.getLogger('SecretWarClient')
    log.addHandler(handler)
    log.propagate = False
    log.setLevel(logging.INFO)
    return log


logger = makeLogger()