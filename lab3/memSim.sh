#!/bin/bash

# Compile the Java program
javac memSim.java
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

# Run the Java program with the provided arguments
java memSim "$@"