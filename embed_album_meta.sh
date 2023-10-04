#!/bin/bash

read -p 'album: ' album
read -p 'artist: ' artist

for file in *
do
    if [[ $file == *.m4a ]]
    then
        filename="${file%.*}"
        exiftool -overwrite_original -Title="$filename" -Album="$album" -Artist="$artist" "$file"
    fi
done

