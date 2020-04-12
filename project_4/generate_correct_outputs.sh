#!/bin/bash

for i in test-*.txt; do
  arrName=(${i//./ })
  arrName=(${arrName[0]//-/ })
  mode=${arrName[2]}
  echo "$(./drone -m $mode < $i > "$i.correct")"
done
