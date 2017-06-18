#!/usr/bin/env bash

# pretty print gphocs results
head -1 trace.tsv | column -t && tail -10 trace.tsv | column -t