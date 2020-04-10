# Project 3 Tools
These tools were developed by @neiljohari during W20 for the SillyQL iteration
of this project. The scripts should be pretty easy to adapt for future
iterations of this project.

# Regression Testing

Use case: I'm in a situation where I pass all tests but have lots of TLEs. I want to optimize my code but don't want my changes breaking existing functionality. 

Instead of manually running every single test I have, I wrote a small bash script to automatically run my own test suite.

Usage:
- Make sure the scripts are executable (`chmod +x ./generate_correct_outputs.sh && chmod +x ./regression_test.sh`)
- Run `./generate_correct_outputs.sh` after altering tests or adding tests, but not after changing your codebase
- Run `./regression_test.sh` to run your tests. If you just get blank lines, your regression test passed. If you get any lines like `Files /dev/fd/# and test-#-table-commands.txt.correct differ` then your changes broke something that `test-#` was testing!
- If you want to run the short input too, add the flag `-s`. If you want to run the long input too, add the flag `-l`.

Notes:
- You should be passing all tests on AG, otherwise chances are you'll be generating faulty outputs and so your regression test doesn't make any sense to perform in the first place
- You need at least decent test coverage (use buggy solutions caught as a metric for this)

# Code Coverage Tool
## Intro
`gcov` is a source code analysis tool (and profiling but we're not using that feature here). It can do things like tell you how many times particular branches were taken, if at all.

One of the W20 TAs (@pgossman) recommended we approach making tests by trying to "paint" our code and basically make sure every line gets hit. This tool helps do exactly that.

It helped me catch 3 more buggy solutions so I figured it's probably worth sharing (I literally just added tests to hit 100% code coverage).

The other tool used, `lcov`, takes the gcov info and makes it into a pretty web page.

## Installation

Gcov comes as a standard utility with gcc. Lcov you need to install, if you have homebrew just do `brew install lcov` and you're set.

## Changes to compiling

You need to compile your executable with `-fprofile-arcs` and `-ftest-coverage`. This will make it so when you run the executable, a couple of files with `*.gcda` and `*.gcno` are created—those contain the information from the coverage report.

If you use the 281 provided Makefile just throw this in as a target:
```
gcov: CXXFLAGS += -fprofile-arcs -ftest-coverage
gcov:
 $(CXX) $(CXXFLAGS) $(SOURCES) -o $(EXECUTABLE)_gcov
```

## Generating the lcov report

Lcov makes its own info file using the gcov reports. The goal here is to run your executable against all your tests, and each time generating an lcov report based off the latest gcov report files. Then, using the `genhtml` command that comes with lcov to create the webpage report.

Here's a script I wrote to do this:
`generate_lcov_report.sh`
```
#!/bin/bash

make gcov 


function generate_lcov_report () {
 ./silly_gcov $2 < $1
 lcov -t "lcov-$1" -o "$1.info" -c -d .
} FILES=""
for i in test-*.txt; do
 generate_lcov_report $i 
 FILES+=$i
 FILES+=".info "
done

genhtml -o res $FILES
```

You need to make it executable before running it: `chmod +x generate_lcov_report.sh`.

Sometimes the script fails if you make changes to your executable. I think it's because gcov report files might be cumulative, so just run `rm *.gcda` and `rm *.gcno`.

## Viewing the report

The report should come out in a directory called `res/`. You can open up the `index.html` page in your browser and it'll work.

## Optional Web Server

If you've got python setup you can also `pip install simple-web-server`. Then, `cd res` and run `python -m http.server`. Now the lcov report is available at `http://0.0.0.0:8000/` in your browser.

## Improvements?

Idk I've never used lcov before today, there's probably a better way to take advantage of the cumulative nature of gcov (if it is? I have no idea). I just found this setup to work for me.

## Video

Since the 281 IA apps were due soon, I kinda just chose to make my video on this stuff. [Here is is if you're interested](https://www.youtube.com/watch?v=s4KDFKhKwe0).

It's more general to gcov and lcov (very brief overview and demo).
