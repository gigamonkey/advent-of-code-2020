#!/bin/bash

day="$1"

script=$(printf "day-%02d.py" "$day")

if [ ! -x "$script" ]; then
    chmod +x "$script"
fi

case "$2" in
    "-s")
        dir="samples"
        ;;
    *)
        dir="inputs"
        ;;
esac

input=$(printf "$dir/day-%02d.txt" "$day")

./$script $input
