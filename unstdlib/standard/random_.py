import logging
import random as _random

log = logging.getLogger(__name__)

try:
    random = _random.SystemRandom()
except NotImplementedError:
    log.warn('random.SystemRandom() is not available. Using random.Random() '
             'instead, this means that things will be less random.')
    random = _random.Random()


__all__ = ['random']
