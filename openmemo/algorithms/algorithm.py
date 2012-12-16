from collections import namedtuple
from enum import Enum

AlgorithmResult = namedtuple('AlgorithmResult', 'next_review alg_data')

GRADES = (0, 1, 2, 3, 4, 5)
PRIORITY_LOW = -1
PRIORITY_MEDIUM = 0
PRIORITY_HIGH = 1
PRIORITIES = (PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH)
DEFAULT_PRIORITY = PRIORITY_MEDIUM
MIN_GRADE = GRADES[0]
MAX_GRADE = GRADES[len(GRADES) - 1]
FINAL_DRILL = 0
MEMORIZED = 1
STATUSES = (FINAL_DRILL, MEMORIZED)

class AlgorithmGlobalData (object):
    """ Defines operations which gather data not associated with the current 
    learning unit in a more global context.
    
    Input data passed to the algorithm describes learning parameters of a single LU.
    Some algorithms require in some cases parameter summaries of more than one LU.
    Other may need a more global data which is known after some intermediate calculations
    (at the beginning of the calculations the algorithm doesn't know if it is 
    doing to request more data and what additional data is required).
    """


class Algorithm (object):
    """ Base class for a repetion scheduling algorithm. 
    
    Keeps a reference to a provider for gathering parameters that are out of scope 
    of the current LU algorithm data. 
    """
    
    def __init__(self, global_data, *args, **kwargs):
        self.global_data = global_data
    
    def schedule(self, grade, alg_data=None, priority=DEFAULT_PRIORITY, now=None, estimated=False, user_data=None):
        """ Calculates next repetition for a LU.
        
        Returns AlgorithmResult.
        """
        raise NotImplementedError()

    