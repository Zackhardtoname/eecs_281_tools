'''\
run submission test files and private test files. optionally, run them with
valgrind. finally, diff the output against the correct output.

note: "NUM..." parameters denote a space-seperated string of test numbers.

by sctodd winter 2020 (shoutout rona)'''
import abc
import argparse
import glob
import re
import shlex
import shutil
import subprocess
import sys
import textwrap

__all__ = ['TestSuite']
epilog = '''\
to get started, name the correct output file the same as its corresponding
input except with 'correct' file extension. place private test files in a
folder called 'tests'. then, subclass TestSuite by setting EXECUTABLE and
implementing get_flags. finally, call your subclass's main classmethod.

"install" this package by symlinking it into your project directory, then you
can import it.

if you want to, install colordiff.

file structure example from p2-market:
./                              submission files (should already be there)
    market_debug                the main program
    test-1-v.txt                runs ./market_debug --verbose < test-1-v.txt \
> tests/test-1-v.out
    test-1-v.correct            correct output for test 1
    tests/                      private test files
        test-1-v.out            output of test 1
        test-10-m.txt           runs ./market_debug --median < tests/\
test-10-m.txt > tests/test-10-m.out
        test-10-m.correct       correct output for test 10
        test-10-m.out           output of test 10
        test-11-error.txt       runs ./market_debug < tests/test-11-error.txt \
>& tests/test-11-error.out
                                and ensures non-zero exit value
        test-11-error.correct   correct output for test 11
        test-11-error.out       output of test 11'''


# returns if valgrind's -s flag is supported
def valgrind_s_flag():
    process = subprocess.run(
        shlex.split('valgrind -s true'),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return not process.returncode


def int_list(string):
    return list(map(int, string.split()))


class Range:
    def __init__(self, string='0'):
        choices = int_list(string)

        if len(choices) == 1:
            self.begin = choices[0]
            self.end = -1
        else:
            self.begin, self.end = choices

    def __contains__(self, n):
        if self.end < 0:
            return self.begin <= n
        else:
            return self.begin <= n <= self.end

    def __repr__(self):
        cls = type(self).__qualname__

        if self.end < 0:
            return f"{cls}('{self.begin!r}')"
        else:
            return f"{cls}('{self.begin!r} {self.end!r}')"


class TestSuite(abc.ABC):
    '''\
the test driver 😎
subclass this class, define EXECUTABLE and get_flags, and call main.
example: TestSuite.main()'''

    VALGRIND = ('valgrind --leak-check=full --show-leak-kinds=all '
                '--error-exitcode=1 ')
    VALGRIND += '-s' if valgrind_s_flag() else '-v'
    DIFF = shutil.which('diff')
    COLORDIFF = shutil.which('colordiff') or DIFF

    @property
    @abc.abstractmethod
    def EXECUTABLE(self):
        '''\
the debug build executable. go ahead and define this as a class variable rather
than a property. example: 'silly_debug'.'''

    @staticmethod
    @abc.abstractmethod
    def get_flags(fname_suffix: str) -> list:
        '''\
return a list of command line flags for the test executable.
get_flags takes the third part of the filename and returns the list of flags
that should be run. for example, if we are processing test-1-sl.txt from
p1-puzzle, then fname_suffix would be 'sl' and we would return
['--stack', '--output list'].'''

    @property
    def _diff(self):
        return self.COLORDIFF if self.color else self.DIFF

    def __init__(self, valgrind=False, color=True, range_=Range(),
                 blacklist=[], ignore_error=[], skip_diff=[],
                 skip_valgrind=[]):
        self.valgrind = valgrind
        self.color = color
        self.blacklist = blacklist
        self.range = range_
        self.ignore_error = ignore_error
        self.skip_diff = skip_diff
        self.skip_valgrind = skip_valgrind

    def run(self) -> int:
        files = []
        files += sorted(glob.glob('test-*-*.txt'))
        files += sorted(glob.glob('tests/test-*-*.txt'))

        for filename in files:
            # split by - or by .
            fname_start, num, *fname_suffix, _ = re.split(r'-|\.', filename)
            num = int(num)
            fname_suffix = '-'.join(fname_suffix)
            returncode = self.test_case(fname_start, num, fname_suffix)

            if returncode and num not in self.ignore_error:
                return returncode

        return 0

    def test_case(self, fname_start, num, fname_suffix) -> int:
        if num in self.blacklist or num not in self.range:
            return 0

        error = fname_suffix == 'error'
        flags = ' '.join(self.get_flags(fname_suffix))
        in_file = f'{fname_start}-{num}-{fname_suffix}.txt'
        out_file = f'tests/test-{num}-{fname_suffix}.out'
        out_redirect = '>&' if fname_suffix == 'error' else '>'
        returncode = self.system(
            f'./{self.EXECUTABLE} {flags} < {in_file} {out_redirect} '
            f'{out_file}',
            valgrind=(self.valgrind
                      and num not in self.skip_valgrind
                      and not error))

        if error:
            if not returncode:
                return not returncode
        elif returncode or num in self.skip_diff:
            return returncode

        correct_file = f'{fname_start}-{num}-{fname_suffix}.correct'
        return self.system(f'{self._diff} -u {correct_file} {out_file}')

    def system(self, cmd, valgrind=False) -> int:
        if valgrind:
            cmd = f'{self.VALGRIND} {cmd}'

        print(cmd, flush=True)
        return subprocess.run(cmd, shell=True).returncode

    @classmethod
    def main_helper(cls, argv) -> int:
        '''the main function except it returns int like C/C++'''
        if type(argv) is str:
            argv = shlex.split(argv)

        nums = '"NUM..."'
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            prog=argv[0], description=__doc__, epilog=epilog)
        valgrind_group = parser.add_mutually_exclusive_group(required=True)
        valgrind_group.add_argument(
            '--valgrind', '-v', action='store_true',
            help='run the tests with valgrind')
        valgrind_group.add_argument(
            '--no-valgrind', '-n', action='store_true',
            help='do not run the tests with valgrind')
        range_group = parser.add_mutually_exclusive_group()
        range_group.add_argument(
            '--range', '-r', type=Range, default=Range(),
            metavar='"BEGIN [END]"',
            help=textwrap.dedent('''\
                specify which tests to run. defaults to all of them.
                omit END to specify there is no end.'''))
        range_group.add_argument(
            '--list', '-l', type=int_list, metavar=nums, default=None,
            help=textwrap.dedent('''\
                specify which tests to run. note: tests still run in
                numerical order despite order provided here.'''))
        parser.add_argument(
            '--blacklist', '-b', type=int_list, metavar=nums, default=[],
            help='skip these tests.')
        parser.add_argument(
            '--ignore-error', '-i', type=int_list, metavar=nums, default=[],
            help=textwrap.dedent('''\
                if an error happens on these tests, continute with the
                other tests.'''))
        parser.add_argument(
            '--skip-diff', '-s', type=int_list, metavar=nums, default=[],
            help='don\'t run diff on these tests.')
        parser.add_argument(
            '--skip-valgrind', '-q', type=int_list, metavar=nums, default=[],
            help='don\'t run valgrind with these tests')
        parser.add_argument(
            '--color', choices=['always', 'auto', 'never'], default='auto',
            help='choose when to show colored diff output.')

        if len(argv) == 1:
            print(parser.format_help())
            return 0

        args = parser.parse_args(argv[1:])
        range_ = args.list if args.list is not None else args.range
        color = sys.stdout.isatty() if args.color == 'auto' \
            else args.color == 'always'

        return cls(
            args.valgrind, color, range_, args.blacklist, args.ignore_error,
            args.skip_diff, args.skip_valgrind,
        ).run()

    @classmethod
    def main(cls):
        '''call this like TestSuite.main() to run the test program'''
        returncode = cls.main_helper(sys.argv)

        if returncode:
            sys.exit(returncode)
