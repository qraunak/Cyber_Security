#!/bin/bash
url="https://www.cse.iitb.ac.in/~akshatka/newpage.html"
flag='false'
while [ $flag = "false" ] ; do

    # Download the content of the URL.
    curl -s "$url" > t1.txt

    # Get the text from the file.
    text=$(cat t1.txt)
    ignore_url="https://tinyurl.com/mr26dzhe"

    # Search for the URL in the text.
    match=$(echo "$text" | grep -oP 'https?://[^ ]*' | grep -v "$ignore_url")

    # If the match is found, print it.
    if [[ -n "$match" ]]; then
        echo "$match"
        url="$match"
    fi

    file=$(find . -maxdepth 1 -type f -name "*.tar")

    if [ -f "$file" ]; then
        echo -ne "\rFlag found: $file"
        echo
        cat "$file"
        echo
        flag_found=true
    fi

done

