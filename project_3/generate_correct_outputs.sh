#!/bin/bash

for i in test-*.txt; do
  echo "$(./silly < $i > "$i.correct")"
done
