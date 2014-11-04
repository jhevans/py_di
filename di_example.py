from logger import PrintLogger, FileLogger
from provisioner import Provisioner

__author__ = 'JohnH.Evans'


def do_some_stuff():
    logger = Provisioner().get_dependency('logger')
    logger.log('Test')


if __name__ == "__main__":
    Provisioner().provision('logger', FileLogger)
    do_some_stuff()
