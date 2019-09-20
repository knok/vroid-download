#!/bin/sh

FILES=$(cd faces; ls)

#echo $FILES

for file in $FILES
do
    convert faces/$file -resize 64x64! fixed/$file
done
