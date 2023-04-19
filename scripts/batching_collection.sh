#!/bin/bash

batch = 300;
i=0; 
for f in *; 
do 
    d=dir_$(printf %03d $((i/batch+1))); 
    mkdir -p $d; 
    mv "$f" $d; 
    let i++; 
done

