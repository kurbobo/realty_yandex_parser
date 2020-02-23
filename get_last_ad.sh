#!/bin/sh
cd ads_texts
ls | grep 'txt' | cut -d '.' -f-1 | sort | tail -n 1