#!/bin/bash

ROOT="AI-Python-Course"
FOLDERS=("notebooks" "data" "src" "results")

mkdir -p $ROOT
for FOLDER in "${FOLDERS[@]}"; do
    mkdir -p "$ROOT/$FOLDER"
done

touch "$ROOT/README.md"
touch "$ROOT/requirements.txt"
touch "$ROOT/Makefile"

echo "The directory AI-Python-Course and its structure were created successfully!"
