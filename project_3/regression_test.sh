#!/bin/bash

# takes 2 args: test input file, correct test output, optional ./silly flags
function run_test () {
  diff -q <(./silly $3 < $1) $2
  rv=$?
  if [ $rv -eq 0 ]
  then
    echo "PASS"
  elif [ $rv -eq 1 ]
  then
    echo "FAIL" 1>&2
  else
    echo "There was an issue with the diff command itself." 1>&2
  fi
}

# run your test suite
for i in test-*.txt; do
  run_test $i "$i.correct"
done

# run the spec given test
run_test "spec_input.txt" "spec_output.txt"

while getopts "hsl" opt; do
  case $opt in
    h)
      echo "Usage ./regression_test [-h] [-s] [-l] [-c]" 
      echo "  options:" 
      echo "    -h outputs this help menu" 
      echo "    -s runs the short input" 
      echo "    -l runs the long input" 
      echo "    -c runs both short and long inputs as well" 
      ;; 
    l)
      echo "Running in long mode (long input)" 
      run_test "long-quiet-input.txt" "long-quiet-output.txt" "-q"
      ;;
    s)
      echo "Running in short mode (short input)" 
      run_test "short-input.txt" "short-output.txt"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
  esac
done

