class svForceExit(Exception):
    """
    This exception actually derives from Python's Exception class to act as an
    exit methodology for the program. This would cause the script to stop all
    operations and start exiting the program. It is explicitly a custom
    exception to guarantee no overlap.
    """
    pass
