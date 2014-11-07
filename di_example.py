from logger import PrintLogger, FileLogger
from feature_broker import FeatureBroker

__author__ = 'JohnH.Evans'


def do_some_stuff():
    logger = FeatureBroker().get_feature('logger')
    logger.log('Test')


if __name__ == "__main__":
    # FeatureBroker().provide('logger', FileLogger)
    FeatureBroker().provide('logger', PrintLogger)
    do_some_stuff()
