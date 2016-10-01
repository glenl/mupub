"""
The main console script entry point.

"""

import sys
from mupub.cli import dispatch

def main():
    """Dispatch with system arguments. """
    return dispatch(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())