#!/bin/bash

# How far off is considered passing for you in FASTTSP? Given as a percentage.
# Default right now is 1% margin of error
TOLERANCE=1

echo "Running regression test suite with a tolerance of $TOLERANCE% for FASTTSP"

# Creates a temp file to store the first line of your program's output
temp_file=$(mktemp)
trap "rm -f $temp_file" 0 2 3 15

# takes 3 args: test input file, correct test output, mode
function run_test () {
  ./drone -m $3 < $1 > $temp_file

  # First let's test that the program outputs the right number of vertices
  # overall
  wc=$( wc -w < $temp_file )
  wc_correct=$( wc -w < $2 )

  if [ "$wc" -ne "$wc_correct" ]
  then
    echo "FAILED $1 ON $3 (word counts differ — wrong number of vertices?)"
    return
  fi

  # Now let's check that the program outputs the right weight
  diff -q <(head -n 1 $temp_file) <(head -n 1 $2) > /dev/null 2>&1

  rv=$?
  if [ $rv -eq 0 ]
  then
    echo "PASSED $1 ON $3"
  elif [ $rv -eq 1 ]
  then
    # Diff isn't enough for FASTTSP weight...
    # We test how far off your weight is from the correct output
    if [[ "$3" == "FASTTSP" ]]
    then
      # Your program's weight
      tmp_output=$(head -n 1 $temp_file)

      # The difference as a positive percentage 
      cost_diff_percent=$( echo "100 * ( ${tmp_output:-0} - $(head -n 1 $2) ) / ($(head -n 1 $2))" | bc -l | sed 's/-//') 

      # Test if difference exceeds tolerance
      if (( $(echo "$cost_diff_percent > $TOLERANCE" | bc -l) ))
      then
        printf "FAILED $1 ON $3 (OFF BY %.3f%%)\n" $cost_diff_percent 1>&2
      else
        printf "PASSED $1 ON $3 (difference of %.3f%% was within tolerance)\n" $cost_diff_percent 
      fi 

    else
      echo "FAILED $1 ON $3" 1>&2
    fi
  else
    echo "There was an issue with the diff command itself." 1>&2
  fi
}

# Run your test suite
for i in test-*.txt; do
  # Infer the mode to run the test with
  arrName=(${i//./ })
  arrName=(${arrName[0]//-/ })
  mode=${arrName[2]}

  run_test $i "$i.correct" $mode
done

# Run the spec given test
run_test "sample-ab.txt" "sample-ab-MST-out.txt" "MST"
run_test "sample-ab.txt" "sample-ab-FASTTSP-out.txt" "FASTTSP"

run_test "sample-c.txt" "sample-c-MST-out.txt" "MST"
run_test "sample-c.txt" "sample-c-FASTTSP-out.txt" "FASTTSP"
run_test "sample-c.txt" "sample-c-OPTTSP-out.txt" "OPTTSP"

run_test "sample-d.txt" "sample-d-MST-out.txt" "MST"
run_test "sample-d.txt" "sample-d-FASTTSP-out.txt" "FASTTSP"
run_test "sample-d.txt" "sample-d-OPTTSP-out.txt" "OPTTSP"

run_test "sample-e.txt" "sample-e-MST-out.txt" "MST"
run_test "sample-e.txt" "sample-e-FASTTSP-out.txt" "FASTTSP"
run_test "sample-e.txt" "sample-e-OPTTSP-out.txt" "OPTTSP"

