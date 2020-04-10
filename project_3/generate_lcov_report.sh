#!/bin/bash

make gcov 


function generate_lcov_report () {
  ./silly_gcov $2 < $1
  lcov -t "lcov-$1" -o "$1.info" -c -d .
}

FILES=""
for i in test-*.txt; do
  generate_lcov_report $i 
  FILES+=$i
  FILES+=".info "
done

genhtml -o res $FILES
