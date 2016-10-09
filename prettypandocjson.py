#! /usr/bin/env python

import sys
import json


def main(arg):
    print(json.dumps(json.loads(arg), indent=2))


if __name__ == '__main__':
    main('\n'.join([line for line in sys.stdin]))
