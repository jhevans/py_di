from logger import PrintLogger
from py_di.injector import Injector

__author__ = 'JohnH.Evans'


def do_some_stuff():
    logger = Injector().get_feature('logger')
    logger.log('Test')


if __name__ == "__main__":
    # Injector().provide('logger', FileLogger)
    Injector().provide('logger', PrintLogger)
    do_some_stuff()
