#!/bin/bash

# Variables
REPO="mwilco03/Fruiti-finder"
BRANCH="main"
DIRECTORY="dockerized"
DEST_DIR="fruitifinder"
# Create a temporary directory
TEMP_DIR=$(mktemp -d)
# Download the archive
curl -L https://github.com/$REPO/archive/$BRANCH.zip -o $TEMP_DIR/repo.zip
# Unzip the specific directory
unzip -q $TEMP_DIR/repo.zip "$REPO-$BRANCH/$DIRECTORY/*" -d $TEMP_DIR
# Move the directory to the destination
mkdir -p $DEST_DIR
mv $TEMP_DIR/$REPO-$BRANCH/$DIRECTORY/* $DEST_DIR/
# Clean up
rm -rf $TEMP_DIR
echo "Directory has been pulled down from $REPO and saved to $DEST_DIR."
cd $DEST_DIR

