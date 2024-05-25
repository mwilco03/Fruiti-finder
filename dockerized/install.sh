#!/bin/bash

# Variables
REPO="mwilco03/Fruiti-finder"
BRANCH="main"
DIRECTORY="dockerized"
DEST_DIR="fruitifinder"

# Function to download a file from GitHub
download_file() {
  local file_url=$1
  local file_path=$2
  echo "Downloading $file_path"
  mkdir -p "$(dirname "$file_path")"
  curl -L "$file_url" -o "$file_path"
}

# Function to traverse and download directory contents
download_directory() {
  local api_url=$1
  local local_dir=$2

  # List directory contents using GitHub API
  contents=$(curl -s "$api_url" | jq -r '.[] | "\(.type) \(.download_url) \(.path)"')

  while IFS= read -r line; do
    type=$(echo $line | cut -d' ' -f1)
    download_url=$(echo $line | cut -d' ' -f2)
    path=$(echo $line | cut -d' ' -f3)
    local_path="$local_dir/$(basename "$path")"

    if [ "$type" = "file" ]; then
      download_file "$download_url" "$local_path"
    elif [ "$type" = "dir" ]; then
      new_api_url="https://api.github.com/repos/$REPO/contents/$path?ref=$BRANCH"
      new_local_dir="$local_dir/$(basename "$path")"
      download_directory "$new_api_url" "$new_local_dir"
    fi
  done <<< "$contents"
}

# Initial API URL
API_URL="https://api.github.com/repos/$REPO/contents/$DIRECTORY?ref=$BRANCH"

# Start downloading the directory
mkdir -p "$DEST_DIR"
download_directory "$API_URL" "$DEST_DIR"

echo "Directory $DIRECTORY has been downloaded to $DEST_DIR."
cd $DEST_DIR
echo "Building the image."
docker build -f ./Dockerfile -t mwilco03/fruitifinder .
echo "Running the container."
docker run -p 9080:9080 --rm -d mwilco03/fruitifinder 
