#!/bin/sh

for f in $(find . -iname "*.py" -not -path "**/.venv/**")
do
    echo "Formatting ${f}..."
    autopep8 ${f} --in-place
done

for f in $(find . -iname "*.rs")
do
    echo "Formatting ${f}..."
    rustfmt ${f}
done