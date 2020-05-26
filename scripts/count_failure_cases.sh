#!/bin/bash

if [ $# -eq 1 ]; then
  gen=$(greadlink -f $1)
else
  echo "Usage: count_failure_cases hypothesis"
fi

cd $(dirname $0)/..

fail=$(ggrep -Pc '^H-[0-9]*\t\-inf' $gen)
total=$(ggrep -Pc '^H-[0-9]*\t' $gen)
rate=$(echo "$fail/$total*100" | bc -l)
printf 'Failure rate: %.2f (%d / %d)\n' $rate $fail $total
