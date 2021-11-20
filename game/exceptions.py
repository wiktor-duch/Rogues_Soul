class ImpossibleAction(Exception):
    '''
    Exception raised when an action is impossible to be performed.

    The reason is given as the exception message.
    '''

class InvalidMap(Exception):
    '''
    Exception raised when the map could not be generated correctly.

    The reason is given as the exception message.
    '''