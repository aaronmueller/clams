#!/bin/bash

for filename in $1/*.txt.p; do
	mv "$filename" "${filename%.txt.p}".txt
done
