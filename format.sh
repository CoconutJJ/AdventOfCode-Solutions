#!/bin/sh

for f in $(find . -iname "*.py" -not -path "**/.venv/**")
do
    echo "Formatting ${f}..."
    autopep8 ${f} --in-place
done