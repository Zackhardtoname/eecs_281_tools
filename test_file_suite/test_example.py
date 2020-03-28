#!/usr/bin/env python3
'''\
here's an example main file. it doesn't actually go in the folder next to
__init__.py etc. this file should go next to your *.cpp files.'''
import test_file_suite


class SillyTestSuite(test_file_suite.TestSuite):
    EXECUTABLE = 'silly_debug'

    @staticmethod
    def get_flags(fname_suffix: str) -> list:
        '''example:
            (fname -> fname_suffix -> flags)
            test-1-table-commands.txt -> 'table-commands' -> []
            tests/test-20-quiet.txt -> 'quiet' -> ['--quiet']'''
        flags = []

        if fname_suffix == 'quiet':
            flags.append('--quiet')

        return flags


if __name__ == '__main__':
    SillyTestSuite.main()
