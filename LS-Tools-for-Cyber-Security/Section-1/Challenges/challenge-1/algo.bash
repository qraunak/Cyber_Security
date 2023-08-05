#!/bin/bash

# Function to decode password using different encodings
encode_password() {
    local password_file=$1
    password_list=(
        $(cat "$password_file" | base64)
        $(cat "$password_file" | base32)
        $(cat "$password_file" | xxd -p)
        $(cat "$password_file")
    )
}

# Function to extract zip file
extract_zip() {
    local zip_file=$1
    local password=$2

    if [ -z "$password" ]; then
        unzip -qq -o "$zip_file" &> /dev/null #d $output 
    else
        unzip -qq -P "$password" -o "$zip_file" &> /dev/null
    fi
}

# Function to extract 7zip file
extract_7zip() {
    local zip_file=$1
    local password=$2

    if [ -z "$password" ]; then
        7z x -y "$zip_file" &> /dev/null #-o$output 
    else
        7z x -y -p"$password" "$zip_file" &> /dev/null
    fi
}

extract_archieve()
{
    local archive_file=$1
    local password=$2
    
    # Get zip type based on extension
    encoding=$(basename "$archive_file" | cut -d'.' -f2)

    case $encoding in 
        zip)
            # extract_7zip $archive_file $output_dir $password  ;;
            extract_zip $archive_file $password ;;
        7z)
            extract_7zip $archive_file $password  ;;
        *)
            echo unexpected archive type: $encoding; return 1;;
    esac
}


# Initial setup
flag_found=false

# Temp Directory
rm -rf work_dir
mkdir -p work_dir
cp *.7z work_dir
cd work_dir
status=0
# Loop until the flag is found
while [ "$flag_found" = false ]; do

    # Get zip file name
    archive_file=$(find . -maxdepth 1  -type f -regex ".*\.\(7z\|zip\)")
    
    # Get password file name
    password_file=$(find . -maxdepth 1 -type f ! -name "*.*")

    # Debug Info
    echo -ne "\r$archive_file <=> $password_file"

    if [[ -e "$password_file" ]]; then
        encode_password $password_file
        for password in "${password_list[@]}"
        do
            extract_archieve $archive_file $password
            status=$?
            if [ $status -eq 0 ] 
            then 
                break 
            fi
        done
    else
        extract_archieve $archive_file 
    fi
    
    # break

    # Clean
    if [ $status -eq 0 ] 
    then
        rm -r $archive_file $password_file
    fi
    
    # Check if the flag file exists
    flag_file=$(find . -maxdepth 1  -type f -name "flag*")
    if [ -f "$flag_file" ]; then
        echo -ne "\rFlag found: $flag_file"
        echo 
        cat $flag_file
        echo 
        flag_found=true
    fi
done

