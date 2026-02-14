#!/bin/bash

FILE="pythonos.py"
URL="https://raw.githubusercontent.com/CharmanderHero190Cloud/PythonOS-Archlinux/main/pythonos.py"

# Function: Print red error
error() {
    echo -e "\e[31m$1\e[0m"
}

# Function: Check internet
check_internet() {
    ping -c 1 8.8.8.8 > /dev/null 2>&1
    return $?
}

echo "Starting update script..."

# If file does NOT exist
if [ ! -f "$FILE" ]; then
    echo "pythonos.py not found."

    if check_internet; then
        echo "Internet detected. Downloading pythonos.py..."
        curl -s -o "$FILE" "$URL"
        echo "Download complete."
    else
        error "You don't have internet connection!"
        exit 1
    fi
else
    echo "pythonos.py found."

    if check_internet; then
        echo "Checking for updates..."

        # Download temporary version
        curl -s -o temp_pythonos.py "$URL"

        # Compare files
        if ! cmp -s "$FILE" temp_pythonos.py; then
            echo "New version detected. Updating..."
            mv temp_pythonos.py "$FILE"
            echo "Updated successfully."
        else
            echo "Already up to date."
            rm temp_pythonos.py
        fi
    else
        echo "No internet. Running local version."
    fi
fi

# Run python file
echo "Running pythonos.py..."
python "$FILE"
