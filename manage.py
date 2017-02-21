#!/usr/bin/env python
import sys

if __name__ == "__main__":
    # import pydevd
    # pydevd.settrace('localhost', port=31337, stdoutToServer=True, stderrToServer=True)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
